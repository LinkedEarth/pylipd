#!/usr/bin/env python3
"""
SPARQL-Optimized LiPD Variable Statistics Updater

Performance optimizations:
1. Load all files in parallel using PyLiPD
2. Use SPARQL queries to get variable values directly
3. Update statistics via SPARQL queries 
4. Use create_lipd for saving (avoiding JSON manipulation)
5. Proper NaN handling with "_NaN_" strings
"""

import os
import sys
import argparse
import json
import numpy as np
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict
import gc
import time
import multiprocessing as mp
import pickle
import tempfile
from concurrent.futures import ProcessPoolExecutor
import shutil

# Add the project root to the path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from pylipd.lipd import LiPD
except ImportError as e:
    print(f"Error importing PyLiPD: {e}")
    print("Please ensure PyLiPD is installed: pip install pylipd")
    sys.exit(1)


class SPARQLOptimizedLiPDStatisticsUpdater:
    def __init__(self, input_dir=None, output_dir="lipd_statistics_updated_sparql"):
        self.input_dir = Path(input_dir) if input_dir else None
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Results storage
        self.update_stats = {
            'total_files_processed': 0,
            'total_variables_processed': 0,
            'variables_with_updates': 0,
            'files_with_updates': 0,
            'update_details': []
        }

    def safe_float_to_json(self, value):
        """Convert float to JSON-safe value, handling NaN."""
        if value is None:
            return None
        if np.isnan(value) or np.isinf(value):
            return "_NaN_"
        return float(value)

    def calculate_statistics_from_values(self, values):
        """Calculate min, max, mean, median from a list of values."""
        try:
            if not values or len(values) == 0:
                return None
            
            # Convert to numeric values
            numeric_values = []
            for v in values:
                if v is not None and v != '' and v != 'null':
                    try:
                        if isinstance(v, (int, float)):
                            numeric_values.append(float(v))
                        elif str(v).lower() not in ('nan', 'null', 'none', '_nan_'):
                            numeric_values.append(float(v))
                    except (ValueError, TypeError):
                        continue
            
            if len(numeric_values) == 0:
                return None
            
            np_values = np.array(numeric_values, dtype=np.float64)
            return {
                'min': self.safe_float_to_json(np.min(np_values)),
                'max': self.safe_float_to_json(np.max(np_values)),
                'mean': self.safe_float_to_json(np.mean(np_values)),
                'median': self.safe_float_to_json(np.median(np_values))
            }
            
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return None

    def needs_update(self, current_value, new_value, tolerance=1e-10):
        """Check if a value needs updating."""
        if current_value is None:
            return True
        if new_value == "_NaN_":
            return current_value != "_NaN_"
        if current_value == "_NaN_":
            return True
        try:
            return abs(float(current_value) - float(new_value)) > tolerance
        except (ValueError, TypeError):
            return True

    def deduplicate_files(self, file_paths):
        """Deduplicate LiPD files based on filename, keeping the newest version."""
        print(f"  Deduplicating {len(file_paths)} files by filename...")
        
        filename_to_files = defaultdict(list)  # filename -> list of (file_path, mtime)
        
        # Group files by name and get modification times
        for file_path in file_paths:
            try:
                filename = file_path.name  # Get just the filename (e.g., "dataset.lpd")
                mtime = file_path.stat().st_mtime  # Get modification time
                filename_to_files[filename].append((file_path, mtime))
            except Exception as e:
                print(f"    Warning: Could not get info for {file_path}: {e}")
                # Include files we can't process to be safe
                filename_to_files[str(file_path)].append((file_path, 0))
        
        # For each filename, keep only the newest version
        unique_files = {}  # filename -> newest_file_path
        duplicate_info = {}  # filename -> list of all file_paths
        
        for filename, file_list in filename_to_files.items():
            # Sort by modification time (newest first)
            file_list.sort(key=lambda x: x[1], reverse=True)
            
            # Keep the newest file
            newest_file = file_list[0][0]
            unique_files[filename] = newest_file
            
            # Track all files for this filename
            all_files = [file_info[0] for file_info in file_list]
            duplicate_info[filename] = all_files
        
        unique_file_paths = list(unique_files.values())
        duplicates_found = len(file_paths) - len(unique_file_paths)
        
        print(f"  Found {len(unique_file_paths)} unique filenames ({duplicates_found} duplicates removed)")
        
        # Log duplicate information
        if duplicates_found > 0:
            print(f"  Duplicate filename examples:")
            duplicate_count = 0
            for filename, paths in duplicate_info.items():
                if len(paths) > 1:
                    print(f"    '{filename}' has {len(paths)} copies:")
                    # Show newest file first, then others
                    for i, path in enumerate(paths[:3]):
                        mtime = path.stat().st_mtime
                        import datetime
                        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                        marker = " ← NEWEST" if i == 0 else ""
                        print(f"      {path} ({mtime_str}){marker}")
                    if len(paths) > 3:
                        print(f"      ... and {len(paths) - 3} more")
                    duplicate_count += 1
                    if duplicate_count >= 5:  # Show max 5 duplicate groups
                        break
        
        return unique_file_paths, filename_to_files, duplicate_info

    def get_all_variable_values_sparql(self, lipd_obj):
        """Get all variable values using SPARQL query."""
        # First, let's try a simple query to see what's available
        simple_query = """
        PREFIX lpd: <http://linked.earth/ontology#>
        SELECT ?s ?p ?o
        WHERE { ?s ?p ?o }
        LIMIT 10
        """
        
        try:
            print("  Testing basic SPARQL connectivity...")
            simple_result, simple_df = lipd_obj.query(simple_query)
            print(f"  Basic query returned tuple with DataFrame shape: {simple_df.shape}")
            print(f"  DataFrame columns: {list(simple_df.columns) if hasattr(simple_df, 'columns') else 'No columns'}")
            if len(simple_df) > 0:
                print(f"  Sample row: {simple_df.iloc[0].to_dict()}")
        except Exception as e:
            print(f"  Basic SPARQL query failed: {e}")
            return []
        
        # Try to find datasets first
        dataset_query = """
        PREFIX lpd: <http://linked.earth/ontology#>
        SELECT ?dataset
        WHERE {
            ?dataset a lpd:Dataset .
        }
        """
        
        try:
            print("  Looking for datasets...")
            dataset_result, dataset_df = lipd_obj.query(dataset_query)
            print(f"  Found {len(dataset_df)} datasets")
        except Exception as e:
            print(f"  Dataset query failed: {e}")
        
        # Now try the full query
        sparql_query = """
        PREFIX lpd: <http://linked.earth/ontology#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?dataset ?variable ?values ?minValue ?maxValue ?meanValue ?medianValue
        WHERE {
            ?dataset a lpd:Dataset .
            { 
                { ?dataset lpd:hasPaleoData ?data } 
                UNION 
                { ?dataset lpd:hasChronData ?data } 
            }
            ?data lpd:hasMeasurementTable ?table .
            ?table lpd:hasVariable ?variable .
            ?variable lpd:hasValues ?values .
            
            OPTIONAL { ?variable lpd:hasMinValue ?minValue }
            OPTIONAL { ?variable lpd:hasMaxValue ?maxValue }
            OPTIONAL { ?variable lpd:hasMeanValue ?meanValue }
            OPTIONAL { ?variable lpd:hasMedianValue ?medianValue }
        }
        """
        
        try:
            print("  Executing main variable query...")
            result, result_df = lipd_obj.query(sparql_query)
            print(f"  Main query returned DataFrame with shape: {result_df.shape}")
            print(f"  DataFrame columns: {list(result_df.columns)}")
            
            # Convert DataFrame to list of dictionaries
            converted_results = []
            for _, row in result_df.iterrows():
                converted_results.append({
                    'dataset': row.get('dataset'),
                    'variable': row.get('variable'),
                    'values': row.get('values'),
                    'minValue': row.get('minValue'),
                    'maxValue': row.get('maxValue'),
                    'meanValue': row.get('meanValue'),
                    'medianValue': row.get('medianValue')
                })
            
            print(f"  Converted to {len(converted_results)} variable records")
            return converted_results
            
        except Exception as e:
            print(f"  Error executing main SPARQL query: {e}")
            return []

    def get_all_variable_values_direct(self, lipd_obj):
        """Fallback method to get variable values directly from datasets."""
        print("  Using direct dataset processing as fallback...")
        variable_results = []
        
        try:
            datasets = lipd_obj.get_datasets()
            print(f"  Processing {len(datasets)} datasets directly...")
            
            for dataset in datasets:
                dataset_name = dataset.getName() or "Unknown"
                
                # Process both paleo and chron data
                for data_type, data_collection in [('paleoData', dataset.getPaleoData()), ('chronData', dataset.getChronData())]:
                    if not data_collection:
                        continue
                        
                    for data_obj in data_collection:
                        for data_table in (data_obj.getMeasurementTables() or []):
                            for variable in (data_table.getVariables() or []):
                                values_str = variable.getValues()
                                if values_str:
                                    variable_result = {
                                        'dataset': dataset_name,
                                        'variable': f"{dataset_name}_{variable.getVariableName() or 'unknown'}",
                                        'values': values_str,
                                        'minValue': variable.getMinValue(),
                                        'maxValue': variable.getMaxValue(),
                                        'meanValue': variable.getMeanValue(),
                                        'medianValue': variable.getMedianValue(),
                                        'variable_obj': variable  # Store the actual variable object for updates
                                    }
                                    variable_results.append(variable_result)
            
            print(f"  Direct processing found {len(variable_results)} variables")
            return variable_results
            
        except Exception as e:
            print(f"  Error in direct dataset processing: {e}")
            return []

    def update_variable_statistics_sparql(self, lipd_obj, variable_uri, new_stats):
        """Update variable statistics using SPARQL update queries."""
        updates_applied = 0
        
        # Prepare values for SPARQL (handle NaN)
        stats_for_sparql = {}
        for stat_name, value in new_stats.items():
            if value == "_NaN_":
                stats_for_sparql[stat_name] = '"_NaN_"'
            elif value is not None:
                stats_for_sparql[stat_name] = f'"{value}"^^xsd:double'
            else:
                stats_for_sparql[stat_name] = None
        
        try:
            # Update each statistic
            for stat_name, sparql_value in stats_for_sparql.items():
                if sparql_value is not None:
                    # Map stat names to SPARQL properties
                    property_map = {
                        'min': 'lpd:hasMinValue',
                        'max': 'lpd:hasMaxValue', 
                        'mean': 'lpd:hasMeanValue',
                        'median': 'lpd:hasMedianValue'
                    }
                    
                    property_uri = property_map.get(stat_name)
                    if property_uri:
                        # Delete existing value
                        delete_query = f"""
                        PREFIX lpd: <http://linked.earth/ontology#>
                        DELETE {{
                            <{variable_uri}> {property_uri} ?oldValue .
                        }}
                        WHERE {{
                            <{variable_uri}> {property_uri} ?oldValue .
                        }}
                        """
                        
                        # Insert new value
                        insert_query = f"""
                        PREFIX lpd: <http://linked.earth/ontology#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA {{
                            <{variable_uri}> {property_uri} {sparql_value} .
                        }}
                        """
                        
                        # Execute the updates
                        lipd_obj.update(delete_query)
                        lipd_obj.update(insert_query)
                        updates_applied += 1
                        
        except Exception as e:
            print(f"Error updating statistics for {variable_uri}: {e}")
        
        return updates_applied

    def update_variable_statistics_direct(self, variable_obj, new_stats):
        """Update variable statistics directly using PyLiPD variable object."""
        updates_applied = 0
        
        try:
            for stat_name, value in new_stats.items():
                # Convert "_NaN_" back to None for PyLiPD
                pylipd_value = None if value == "_NaN_" else value
                
                if stat_name == 'min':
                    variable_obj.setMinValue(pylipd_value)
                    updates_applied += 1
                elif stat_name == 'max':
                    variable_obj.setMaxValue(pylipd_value)
                    updates_applied += 1
                elif stat_name == 'mean':
                    variable_obj.setMeanValue(pylipd_value)
                    updates_applied += 1
                elif stat_name == 'median':
                    variable_obj.setMedianValue(pylipd_value)
                    updates_applied += 1
                    
        except Exception as e:
            print(f"  Error updating variable statistics directly: {e}")
        
        return updates_applied

    def process_batch_variables(self, lipd_obj, variable_results, batch_file_paths, total_stats):
        """Process variables for a single batch and return datasets with updates."""
        batch_datasets_with_updates = defaultdict(list)
        
        # Process each variable result in this batch
        for result in tqdm(variable_results, desc="Processing variables"):
            variable_uri = "unknown"  # Initialize to avoid scope issues
            try:
                # Handle different result formats
                if hasattr(result, 'get'):
                    # Dictionary-like access
                    dataset_uri = result.get('dataset')
                    variable_uri = result.get('variable') or "unknown"
                    values_json = result.get('values')
                    current_stats = {
                        'min': result.get('minValue'),
                        'max': result.get('maxValue'),
                        'mean': result.get('meanValue'),
                        'median': result.get('medianValue')
                    }
                elif hasattr(result, '__getitem__'):
                    # Index-based access (like SPARQLResult)
                    try:
                        dataset_uri = result[0] if len(result) > 0 else None
                        variable_uri = result[1] if len(result) > 1 else "unknown"
                        values_json = result[2] if len(result) > 2 else None
                        current_stats = {
                            'min': result[3] if len(result) > 3 else None,
                            'max': result[4] if len(result) > 4 else None,
                            'mean': result[5] if len(result) > 5 else None,
                            'median': result[6] if len(result) > 6 else None
                        }
                    except (IndexError, TypeError):
                        print(f"    Warning: Could not parse result format: {type(result)}")
                        continue
                else:
                    print(f"    Warning: Unknown result format: {type(result)}")
                    continue
                
                total_stats['total_variables'] += 1
                
                if values_json is not None:
                    # Handle pandas Series or other types
                    if hasattr(values_json, 'iloc'):
                        # It's a pandas Series, get the actual value
                        values_json = values_json.iloc[0] if len(values_json) > 0 else None
                    
                    if values_json is not None:
                        # Parse the values JSON
                        try:
                            values = json.loads(values_json) if isinstance(values_json, str) else values_json
                        except:
                            values = values_json
                    else:
                        values = None
                    
                    # Calculate new statistics
                    calculated_stats = self.calculate_statistics_from_values(values)
                    
                    if calculated_stats:
                        # Check which statistics need updating
                        stats_to_update = {}
                        for stat_name, new_value in calculated_stats.items():
                            current_value = current_stats.get(stat_name)
                            if self.needs_update(current_value, new_value):
                                stats_to_update[stat_name] = new_value
                        
                        if stats_to_update:
                            # Update the statistics - try SPARQL first, then direct method
                            updates_applied = 0
                            
                            if 'variable_obj' in result:
                                # Direct method - update the variable object directly
                                updates_applied = self.update_variable_statistics_direct(
                                    result['variable_obj'], stats_to_update
                                )
                            else:
                                # SPARQL method
                                updates_applied = self.update_variable_statistics_sparql(
                                    lipd_obj, variable_uri, stats_to_update
                                )
                            
                            if updates_applied > 0:
                                total_stats['variables_updated'] += updates_applied
                                batch_datasets_with_updates[dataset_uri].append({
                                    'variable_uri': variable_uri,
                                    'updates': stats_to_update,
                                    'updates_applied': updates_applied
                                })
                
            except Exception as e:
                error_msg = f"Error processing variable {variable_uri}: {e}"
                total_stats['errors'].append(error_msg)
                print(f"    Warning: {error_msg}")
        
        return batch_datasets_with_updates

    def process_all_files_with_sparql(self, file_paths, batch_size=500):
        """Load all files and process using SPARQL queries in batches."""
        print(f"Processing {len(file_paths)} files...")
        
        total_stats = {
            'files_processed': 0,
            'files_with_updates': 0,
            'total_variables': 0,
            'variables_updated': 0,
            'errors': [],
            'duplicates_removed': 0,
            'unique_files_loaded': 0,
            'batches_processed': 0
        }
        
        try:
            # Deduplicate files first
            unique_file_paths, filename_to_files, duplicate_info = self.deduplicate_files(file_paths)
            total_stats['duplicates_removed'] = len(file_paths) - len(unique_file_paths)
            total_stats['unique_files_loaded'] = len(unique_file_paths)
            
            # Process files in batches
            num_batches = (len(unique_file_paths) + batch_size - 1) // batch_size
            print(f"  Processing {len(unique_file_paths)} unique files in {num_batches} batches of {batch_size}...")
            
            # Group results by dataset for processing across all batches
            all_datasets_with_updates = defaultdict(list)
            
            for batch_num in range(num_batches):
                start_idx = batch_num * batch_size
                end_idx = min((batch_num + 1) * batch_size, len(unique_file_paths))
                batch_file_paths = unique_file_paths[start_idx:end_idx]
                
                print(f"\n  Batch {batch_num + 1}/{num_batches}: Loading {len(batch_file_paths)} files...")
                
                # Convert file paths to strings for this batch
                file_path_strings = [str(fp) for fp in batch_file_paths]
                
                # Load this batch with parallel processing
                L = LiPD()
                L.load(file_path_strings, parallel=True)
                
                print(f"    Querying variables in batch {batch_num + 1}...")
                # Get all variable information using SPARQL for this batch
                variable_results = self.get_all_variable_values_sparql(L)
                print(f"    Found {len(variable_results)} variables in batch {batch_num + 1}")
                
                # If SPARQL failed, fall back to direct dataset processing
                if len(variable_results) == 0:
                    print(f"    SPARQL returned no results for batch {batch_num + 1}, falling back to direct processing...")
                    variable_results = self.get_all_variable_values_direct(L)
                    print(f"    Direct processing found {len(variable_results)} variables in batch {batch_num + 1}")
                
                # Process variables in this batch
                batch_datasets_with_updates = self.process_batch_variables(
                    L, variable_results, batch_file_paths, total_stats
                )
                
                # Merge batch results into overall results
                for dataset_uri, updates in batch_datasets_with_updates.items():
                    all_datasets_with_updates[dataset_uri].extend(updates)
                
                # Save updated datasets from this batch
                if batch_datasets_with_updates:
                    print(f"    Saving {len(batch_datasets_with_updates)} updated datasets from batch {batch_num + 1}...")
                    self.save_updated_datasets_sparql(L, batch_datasets_with_updates, batch_file_paths, total_stats)
                
                total_stats['batches_processed'] += 1
                print(f"    Completed batch {batch_num + 1}/{num_batches}")
            
            # Final consolidation
            total_stats['files_with_updates'] = len(all_datasets_with_updates)
            total_stats['files_processed'] = len(unique_file_paths)
            
            print(f"\n  Completed all {num_batches} batches!")
            print(f"  Total datasets with updates: {len(all_datasets_with_updates)}")
            
        except Exception as e:
            total_stats['errors'].append(f"Global processing error: {e}")
            print(f"Error during SPARQL processing: {e}")
        
        return total_stats

    def save_updated_datasets_sparql(self, lipd_obj, datasets_with_updates, original_file_paths, total_stats):
        """Save datasets that have been updated via SPARQL - PROCESS ISOLATION VERSION with file management."""
        
        print(f"    Managing {len(original_file_paths)} total files...")
        
        # Create a mapping from dataset URI to file path (optimized)
        dataset_to_file = {}
        for file_path in original_file_paths:
            file_stem = file_path.stem
            dataset_to_file[file_stem] = file_path
        
        # Get all datasets from the LiPD object once
        datasets = lipd_obj.get_datasets()
        print(f"    Processing {len(datasets)} datasets from LiPD object...")
        
        # Create output directory once
        output_dir_path = self.output_dir / "updated_files"
        output_dir_path.mkdir(parents=True, exist_ok=True)
        
        # Pre-filter datasets that need saving and check existing files
        datasets_to_save = []
        datasets_to_copy = []  # Non-updated files to copy
        files_already_exist = []
        
        for dataset in datasets:
            dataset_name = dataset.getName() or "Unknown"
            output_file_path = output_dir_path / f"{dataset_name}.lpd"
            
            # Check if output file already exists
            if output_file_path.exists():
                files_already_exist.append(dataset_name)
                continue
            
            # Check if this dataset has updates
            has_updates = (dataset_name in datasets_with_updates or 
                          any(dataset_name in str(dataset_uri) for dataset_uri in datasets_with_updates.keys()))
            
            if has_updates and dataset_name in dataset_to_file:
                datasets_to_save.append((dataset, dataset_name))
            elif dataset_name in dataset_to_file:
                # No updates but we should copy the original file
                original_file = dataset_to_file[dataset_name]
                datasets_to_copy.append((original_file, dataset_name))
        
        print(f"    Found {len(datasets_to_save)} datasets that need updating")
        print(f"    Found {len(datasets_to_copy)} datasets to copy (no updates)")
        print(f"    Skipping {len(files_already_exist)} files (already exist in output)")
        
        # Copy non-updated files first (fast operation)
        if datasets_to_copy:
            print(f"    Copying {len(datasets_to_copy)} non-updated files...")
            copied_count = 0
            for original_file, dataset_name in tqdm(datasets_to_copy, desc="Copying files"):
                try:
                    output_file_path = output_dir_path / f"{dataset_name}.lpd"
                    shutil.copy2(original_file, output_file_path)
                    copied_count += 1
                except Exception as e:
                    error_msg = f"Copy error for {dataset_name}: {e}"
                    total_stats['errors'].append(error_msg)
                    print(f"    ✗ Error copying {dataset_name}: {e}")
            
            print(f"    ✓ Copied {copied_count} non-updated files")
        
        # Process updated datasets if any
        if not datasets_to_save:
            print("    No datasets need updating after filtering")
            return
        
        # PROCESS ISOLATION: Serialize datasets and use separate processes
        batch_size = 20  # Larger batches since each process is isolated
        num_batches = (len(datasets_to_save) + batch_size - 1) // batch_size
        
        print(f"    Using process isolation with {num_batches} batches of {batch_size} datasets")
        
        # Prepare batches with serialized datasets
        batches = []
        for batch_idx in range(num_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(datasets_to_save))
            batch_datasets = datasets_to_save[start_idx:end_idx]
            
            # Serialize datasets for inter-process communication
            batch_data = []
            for dataset, dataset_name in batch_datasets:
                try:
                    dataset_pickle = pickle.dumps(dataset)
                    batch_data.append((dataset_pickle, dataset_name))
                except Exception as e:
                    print(f"    Warning: Could not serialize dataset {dataset_name}: {e}")
                    error_msg = f"Serialization error for dataset {dataset_name}: {e}"
                    total_stats['errors'].append(error_msg)
            
            if batch_data:  # Only add non-empty batches
                batches.append((batch_data, str(output_dir_path), batch_idx + 1, num_batches))
        
        print(f"    Prepared {len(batches)} batches for process isolation")
        
        if not batches:
            print("    No batches to process after serialization")
            return
        
        # Use ProcessPoolExecutor for process isolation
        max_workers = min(4, mp.cpu_count(), len(batches))  # Limit concurrent processes
        print(f"    Using {max_workers} worker processes for optimal performance")
        
        saved_count = 0
        skipped_in_workers = 0
        total_errors = []
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all batches
            future_to_batch = {executor.submit(save_dataset_batch_worker, batch): batch for batch in batches}
            
            # Process results as they complete
            for future in tqdm(future_to_batch, desc="Processing batches"):
                try:
                    result = future.result(timeout=300)  # 5 minute timeout per batch
                    
                    if result['success']:
                        batch_saved = result['saved_count']
                        batch_skipped = result.get('skipped_count', 0)
                        saved_count += batch_saved
                        skipped_in_workers += batch_skipped
                        total_errors.extend(result['errors'])
                        
                        status_msg = f"    ✓ Batch {result['batch_idx']} completed: {batch_saved} saved"
                        if batch_skipped > 0:
                            status_msg += f", {batch_skipped} skipped"
                        print(status_msg)
                        
                        # Report progress
                        if saved_count % 20 == 0:
                            print(f"    ✓ Total saved so far: {saved_count} datasets")
                    else:
                        print(f"    ✗ Batch {result['batch_idx']} failed")
                        total_errors.extend(result['errors'])
                        
                except Exception as e:
                    batch_info = future_to_batch[future]
                    batch_idx = batch_info[2]  # batch_idx from args
                    error_msg = f"Process error for batch {batch_idx}: {e}"
                    total_errors.append(error_msg)
                    print(f"    ✗ Process error for batch {batch_idx}: {e}")
        
        # Update total stats
        total_stats['errors'].extend(total_errors)
        
        print(f"    ✓ Process isolation complete! Updated {saved_count} datasets")
        if datasets_to_copy:
            print(f"    ✓ Copied {len(datasets_to_copy)} non-updated datasets")
        total_skipped = len(files_already_exist) + skipped_in_workers
        if total_skipped > 0:
            print(f"    ✓ Skipped {total_skipped} existing files ({len(files_already_exist)} pre-filtered, {skipped_in_workers} in workers)")
        if total_errors:
            print(f"    ⚠ Encountered {len(total_errors)} errors during processing")
        
        # Summary of all file operations
        total_processed = saved_count + len(datasets_to_copy) + total_skipped
        print(f"    📊 Summary: {total_processed} total files - {saved_count} updated, {len(datasets_to_copy)} copied, {total_skipped} skipped")

    def run_sparql_optimized_update_process(self):
        """Run the SPARQL-optimized statistics update process."""
        print("Starting SPARQL-Optimized LiPD Variable Statistics Update Process")
        print("=" * 68)
        
        if not self.input_dir:
            print("Error: Input directory is required")
            return
        
        # Find all LiPD files
        lipd_files = list(self.input_dir.rglob("*.lpd"))
        if not lipd_files:
            print(f"No LiPD files found in {self.input_dir}")
            return
        
        print(f"Found {len(lipd_files)} LiPD files")
        
        # Process all files using SPARQL optimization
        process_stats = self.process_all_files_with_sparql(lipd_files)
        
        # Update global stats
        self.update_stats.update({
            'total_files_processed': process_stats['files_processed'],
            'total_variables_processed': process_stats['total_variables'],
            'variables_with_updates': process_stats['variables_updated'],
            'files_with_updates': process_stats['files_with_updates']
        })
        
        # Generate simple report
        self.generate_simple_report(process_stats)
        
        print("\n" + "=" * 68)
        print("SPARQL-Optimized Statistics Update Process Complete!")
        print(f"Total files found: {len(lipd_files)}")
        print(f"Unique files loaded: {process_stats.get('unique_files_loaded', 'N/A')}")
        print(f"Duplicates removed: {process_stats.get('duplicates_removed', 'N/A')}")
        print(f"Batches processed: {process_stats.get('batches_processed', 'N/A')}")
        print(f"Files processed: {process_stats['files_processed']}")
        print(f"Files updated: {process_stats['files_with_updates']}")
        print(f"Variables processed: {process_stats['total_variables']}")
        print(f"Variables updated: {process_stats['variables_updated']}")
        print(f"Errors: {len(process_stats['errors'])}")
        print(f"Updated files saved to: {self.output_dir / 'updated_files'}")

    def generate_simple_report(self, process_stats):
        """Generate a simple performance report."""
        report_path = self.output_dir / "sparql_optimized_update_report.txt"
        
        with open(report_path, 'w') as f:
            f.write("SPARQL-Optimized LiPD Variable Statistics Update Report\n")
            f.write("=" * 58 + "\n\n")
            
            f.write(f"Unique files loaded: {process_stats.get('unique_files_loaded', 'N/A')}\n")
            f.write(f"Duplicates removed: {process_stats.get('duplicates_removed', 'N/A')}\n")
            f.write(f"Files processed: {process_stats['files_processed']}\n")
            f.write(f"Files updated: {process_stats['files_with_updates']}\n")
            f.write(f"Variables processed: {process_stats['total_variables']}\n")
            f.write(f"Variables updated: {process_stats['variables_updated']}\n")
            f.write(f"Errors encountered: {len(process_stats['errors'])}\n\n")
            
            if process_stats['errors']:
                f.write("Errors:\n")
                for error in process_stats['errors'][:20]:
                    f.write(f"  {error}\n")
        
        print(f"Report generated: {report_path}")


def save_dataset_batch_worker(args):
    """Worker function to save a batch of datasets in an isolated process."""
    batch_data, output_dir_path, batch_idx, total_batches = args
    
    try:
        # Import in worker process to ensure clean state
        from pylipd.lipd import LiPD
        from pathlib import Path
        
        results = []
        saved_count = 0
        skipped_count = 0
        errors = []
        
        # Create a fresh LiPD object in this isolated process
        tempLiPD = LiPD()
        
        for dataset_pickle, dataset_name in batch_data:
            try:
                # Create output file path
                output_file_path = Path(output_dir_path) / f"{dataset_name}.lpd"
                
                # Double-check if file already exists (race condition protection)
                if output_file_path.exists():
                    skipped_count += 1
                    results.append((True, dataset_name, "skipped_existing"))
                    continue
                
                # Deserialize the dataset
                dataset = pickle.loads(dataset_pickle)
                
                # Clear and load dataset
                tempLiPD.clear()
                tempLiPD.load_datasets([dataset])
                
                # Save the dataset
                tempLiPD.create_lipd(dataset_name, str(output_file_path))
                
                saved_count += 1
                results.append((True, dataset_name, None))
                
            except Exception as e:
                error_msg = f"Save error for dataset {dataset_name}: {str(e)}"
                errors.append(error_msg)
                results.append((False, dataset_name, error_msg))
        
        return {
            'batch_idx': batch_idx,
            'saved_count': saved_count,
            'skipped_count': skipped_count,
            'results': results,
            'errors': errors,
            'success': True
        }
        
    except Exception as e:
        return {
            'batch_idx': batch_idx,
            'saved_count': 0,
            'skipped_count': 0,
            'results': [],
            'errors': [f"Batch {batch_idx} worker error: {str(e)}"],
            'success': False
        }


def main():
    parser = argparse.ArgumentParser(
        description="SPARQL-optimized update of variable statistics in LiPD files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process existing directory of LiPD files (SPARQL-optimized)
  python analyze_compilations_sparql.py --input-dir /path/to/lipd/files

  # Specify custom output directory
  python analyze_compilations_sparql.py --output-dir /path/to/output --input-dir /path/to/input
        """
    )
    
    parser.add_argument(
        '--input-dir',
        type=str,
        required=True,
        help='Directory containing LiPD files to process'
    )
    
    parser.add_argument(
        '--output-dir', 
        type=str,
        default='lipd_statistics_updated_sparql',
        help='Output directory for results and updated files (default: lipd_statistics_updated_sparql)'
    )
    
    args = parser.parse_args()
    
    # Create and run the SPARQL-optimized updater
    updater = SPARQLOptimizedLiPDStatisticsUpdater(
        input_dir=args.input_dir,
        output_dir=args.output_dir
    )
    
    try:
        updater.run_sparql_optimized_update_process()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 