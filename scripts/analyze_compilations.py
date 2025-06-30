#!/usr/bin/env python3
"""
Compilation Analysis Script for LiPDVerse

This script:
1. Queries GraphDB repository to get compilation names and dataset counts
2. Analyzes LiPD files from a local input directory  
3. Loads LiPD files using PyLiPD and analyzes compilation assignments
4. Generates reports on compilation consistency and coverage

Usage:
    python analyze_compilations.py --input-dir INPUT_DIR [--output-dir OUTPUT_DIR] [--sparql-endpoint ENDPOINT]
"""

import os
import sys
import argparse
import requests
import json
from pathlib import Path
import pandas as pd
from collections import defaultdict, Counter
import csv

from pylipd.lipd import LiPD


class CompilationAnalyzer:
    def __init__(self, sparql_endpoint, input_dir, output_dir):
        self.sparql_endpoint = sparql_endpoint
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate input directory
        if not self.input_dir.exists():
            raise ValueError(f"Input directory does not exist: {input_dir}")
        if not self.input_dir.is_dir():
            raise ValueError(f"Input path is not a directory: {input_dir}")
        
        # Results storage
        self.graphdb_compilations = {}
        self.local_compilations = {}
        self.lipd_analysis = {}
        
        # Mapping of dataset -> collections info
        self.local_dataset_info: dict[str, dict[str, set]] = defaultdict(lambda: {
            'dir_comps': set(),      # compilations inferred from directory structure
            'lipd_comps': set()      # compilations embedded within LiPD file
        })

        # GraphDB mapping dataset -> compilations
        self.graphdb_dataset_compilations: dict[str, set] = defaultdict(set)
        
    def execute_sparql_query(self):
        """
        Execute SPARQL query to get compilation names and dataset counts from GraphDB.
        
        Returns
        -------
        dict
            Dictionary mapping compilation names to dataset counts
        """
        query = """
        PREFIX le: <http://linked.earth/ontology#>

        SELECT ?compilationName (COUNT(DISTINCT ?dataset) AS ?numberOfDatasets)
        WHERE {
          ?compilation a le:Compilation .
          ?compilation le:hasName ?compilationName .
          ?variable le:partOfCompilation ?compilation .
          ?dataTable le:hasVariable ?variable .
          ?paleoData le:hasMeasurementTable ?dataTable .
          ?dataset le:hasPaleoData ?paleoData 
        }
        GROUP BY ?compilationName
        ORDER BY ?compilationName
        """
        
        print(f"Executing SPARQL query against: {self.sparql_endpoint}")
        
        try:
            response = requests.post(
                self.sparql_endpoint,
                data={
                    'query': query,
                    'format': 'application/sparql-results+json'
                },
                headers={
                    'Accept': 'application/sparql-results+json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                timeout=60
            )
            response.raise_for_status()
            
            results = response.json()
            compilations = {}
            
            for binding in results['results']['bindings']:
                compilation_name = binding['compilationName']['value']
                dataset_count = int(binding['numberOfDatasets']['value'])
                compilations[compilation_name] = dataset_count
            
            self.graphdb_compilations = compilations
            print(f"Found {len(compilations)} compilations in GraphDB:")
            for name, count in sorted(compilations.items()):
                print(f"  - {name}: {count} datasets")
                
            return compilations
            
        except Exception as e:
            print(f"Error executing SPARQL query: {e}")
            raise

    def fetch_graphdb_dataset_compilations(self):
        """Fetch dataset-to-compilation mapping from GraphDB and populate
        self.graphdb_dataset_compilations.
        """

        dataset_query = """
        PREFIX le: <http://linked.earth/ontology#>

        SELECT ?datasetName ?compilationName
        WHERE {
          ?compilation a le:Compilation .
          ?compilation le:hasName ?compilationName .
          ?variable le:partOfCompilation ?compilation .
          ?dataTable le:hasVariable ?variable .
          ?paleoData le:hasMeasurementTable ?dataTable .
          ?dataset le:hasPaleoData ?paleoData .
          ?dataset le:hasName ?datasetName .
        }
        """

        print("Fetching dataset-compilation mapping from GraphDB…")

        try:
            response = requests.post(
                self.sparql_endpoint,
                data={'query': dataset_query, 'format': 'application/sparql-results+json'},
                headers={'Accept': 'application/sparql-results+json', 'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=120
            )
            response.raise_for_status()

            results = response.json()
            count = 0
            for binding in results['results']['bindings']:
                dsname = binding['datasetName']['value'] if 'datasetName' in binding else None
                comp = binding['compilationName']['value']
                if dsname:
                    self.graphdb_dataset_compilations[dsname].add(comp)
                    count += 1
            print(f"  Retrieved compilation info for {len(self.graphdb_dataset_compilations)} datasets from GraphDB.")
        except Exception as e:
            print(f"Error fetching dataset-compilation mapping: {e}")
            # Leave mapping empty if fails

    def scan_input_directory(self):
        """
        Scan the input directory for LiPD files and organize them by compilation.
        
        Returns
        -------
        dict
            Dictionary mapping compilation names to directories containing LiPD files
        """
        print(f"Scanning input directory: {self.input_dir}")
        
        compilations = {}
        
        # Look for LiPD files in the input directory structure
        # Support both flat structure and compilation subdirectories
        
        # Check if input directory contains LiPD files directly
        lipd_files = list(self.input_dir.glob("*.lpd"))
        if lipd_files:
            # Flat structure - treat as single compilation
            comp_name = self.input_dir.name
            compilations[comp_name] = str(self.input_dir)
            print(f"  Found {len(lipd_files)} LiPD files in flat structure: {comp_name}")
        else:
            # Look for subdirectories containing LiPD files
            for subdir in self.input_dir.iterdir():
                if subdir.is_dir():
                    lipd_files = list(subdir.glob("*.lpd"))
                    if lipd_files:
                        comp_name = subdir.name
                        compilations[comp_name] = str(subdir)
                        print(f"  Found {len(lipd_files)} LiPD files in compilation: {comp_name}")
        
        if not compilations:
            print("  No LiPD files found in input directory")
            return {}
        
        self.local_compilations = compilations
        print(f"Found {len(compilations)} compilation(s) with LiPD files")
        return compilations

    def analyze_lipd_compilation(self, compilation_name, lipd_dir):
        """
        Load LiPD files and analyze compilation assignments.
        
        Parameters
        ----------
        compilation_name : str
            Expected compilation name
        lipd_dir : str
            Directory containing LiPD files
            
        Returns
        -------
        dict
            Analysis results
        """
        print(f"Analyzing LiPD files for compilation: {compilation_name}")
        
        try:
            # Load LiPD files
            L = LiPD()
            L.load_from_dir(lipd_dir, parallel=True)
            
            datasets = L.get_datasets()
            total_datasets = len(datasets)
            
            analysis = {
                'compilation_name': compilation_name,
                'lipd_directory': lipd_dir,
                'total_datasets': total_datasets,
                'datasets_with_compilation': 0,
                'datasets_without_compilation': 0,
                'compilation_matches': 0,
                'compilation_mismatches': 0,
                'found_compilations': Counter(),
                'datasets_by_compilation': defaultdict(list),
                'datasets_without_compilation_list': [],
                'compilation_mismatch_list': []
            }
            
            print(f"  Loaded {total_datasets} datasets")
            
            for dataset in datasets:
                dataset_name = dataset.getName() or "Unknown"
                
                # Check for compilation assignment
                try:
                    # Look for variables with partOfCompilation
                    # Check paleo data
                    compilations_found = set()
                    for paleo_data in dataset.getPaleoData() or []:
                        for data_table in paleo_data.getMeasurementTables() or []:
                            for variable in data_table.getVariables() or []:
                                part_of_compilations = variable.getPartOfCompilations()
                                if part_of_compilations:
                                    # Handle both single compilation and multiple compilations
                                    if isinstance(part_of_compilations, list):
                                        for comp in part_of_compilations:
                                            if hasattr(comp, 'getName'):
                                                compilations_found.add(comp.getName())
                                            else:
                                                compilations_found.add(str(comp))
                                    else:
                                        # Single compilation (backward compatibility)
                                        if hasattr(part_of_compilations, 'getName'):
                                            compilations_found.add(part_of_compilations.getName())
                                        else:
                                            compilations_found.add(str(part_of_compilations))
                    
                    # Convert set to list for processing
                    compilations_found = list(compilations_found)
                    
                    if compilations_found:
                        analysis['datasets_with_compilation'] += 1
                        
                        # Track all found compilations
                        for comp_found in compilations_found:
                            analysis['found_compilations'][comp_found] += 1
                            analysis['datasets_by_compilation'][comp_found].append(dataset_name)
                        
                        # Check if expected compilation is in the found compilations
                        if compilation_name in compilations_found:
                            analysis['compilation_matches'] += 1
                        else:
                            analysis['compilation_mismatches'] += 1
                            analysis['compilation_mismatch_list'].append({
                                'dataset': dataset_name,
                                'expected': compilation_name,
                                'found': ', '.join(compilations_found)
                            })
                    else:
                        analysis['datasets_without_compilation'] += 1
                        analysis['datasets_without_compilation_list'].append(dataset_name)
                        
                    # Update local_dataset_info
                    self.local_dataset_info[dataset_name]['dir_comps'].add(compilation_name)
                    if compilations_found:
                        for comp_found in compilations_found:
                            self.local_dataset_info[dataset_name]['lipd_comps'].add(comp_found)
                    
                except Exception as e:
                    print(f"    Error analyzing dataset {dataset_name}: {e}")
                    analysis['datasets_without_compilation'] += 1
                    analysis['datasets_without_compilation_list'].append(dataset_name)
            
            print(f"  Analysis complete:")
            print(f"    - Datasets with compilation: {analysis['datasets_with_compilation']}")
            print(f"    - Datasets without compilation: {analysis['datasets_without_compilation']}")
            print(f"    - Compilation matches: {analysis['compilation_matches']}")
            print(f"    - Compilation mismatches: {analysis['compilation_mismatches']}")
            
            self.lipd_analysis[compilation_name] = analysis
            return analysis
            
        except Exception as e:
            print(f"  Error analyzing LiPD files: {e}")
            return None

    def generate_report(self):
        """
        Generate comprehensive analysis report.
        """
        report_path = self.output_dir / "compilation_analysis_report.txt"
        
        with open(report_path, 'w') as f:
            f.write("LiPDVerse Compilation Analysis Report\n")
            f.write("=" * 50 + "\n\n")
            
            # GraphDB Results
            f.write("1. GraphDB Compilation Query Results\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total compilations found: {len(self.graphdb_compilations)}\n\n")
            
            for comp_name, dataset_count in sorted(self.graphdb_compilations.items()):
                f.write(f"  {comp_name}: {dataset_count} datasets\n")
            f.write("\n")
            
            # Local Results
            f.write("2. Local Compilation Analysis\n")
            f.write("-" * 35 + "\n")
            f.write(f"Total compilations found: {len(self.local_compilations)}\n\n")
            
            for comp_name in sorted(self.local_compilations.keys()):
                f.write(f"  ✓ {comp_name}\n")
            
            missing_compilations = set(self.graphdb_compilations.keys()) - set(self.local_compilations.keys())
            if missing_compilations:
                f.write(f"\nCompilations in GraphDB but not found locally: {len(missing_compilations)}\n")
                for comp_name in sorted(missing_compilations):
                    f.write(f"  ✗ {comp_name}\n")
            f.write("\n")
            
            # LiPD Analysis Results
            f.write("3. LiPD File Analysis\n")
            f.write("-" * 25 + "\n")
            
            for comp_name, analysis in self.lipd_analysis.items():
                f.write(f"\nCompilation: {comp_name}\n")
                f.write(f"  Total datasets: {analysis['total_datasets']}\n")
                f.write(f"  Datasets with compilation: {analysis['datasets_with_compilation']}\n")
                f.write(f"  Datasets without compilation: {analysis['datasets_without_compilation']}\n")
                f.write(f"  Compilation matches: {analysis['compilation_matches']}\n")
                f.write(f"  Compilation mismatches: {analysis['compilation_mismatches']}\n")
                
                if analysis['found_compilations']:
                    f.write(f"  Found compilations:\n")
                    for found_comp, count in analysis['found_compilations'].most_common():
                        f.write(f"    - {found_comp}: {count} datasets\n")
                
                if analysis['datasets_without_compilation_list']:
                    f.write(f"  Datasets without compilation assignment:\n")
                    for dataset in analysis['datasets_without_compilation_list'][:10]:  # Show first 10
                        f.write(f"    - {dataset}\n")
                    if len(analysis['datasets_without_compilation_list']) > 10:
                        f.write(f"    ... and {len(analysis['datasets_without_compilation_list']) - 10} more\n")
                
                if analysis['compilation_mismatch_list']:
                    f.write(f"  Compilation mismatches:\n")
                    for mismatch in analysis['compilation_mismatch_list'][:10]:  # Show first 10
                        f.write(f"    - {mismatch['dataset']}: expected '{mismatch['expected']}', found '{mismatch['found']}'\n")
                    if len(analysis['compilation_mismatch_list']) > 10:
                        f.write(f"    ... and {len(analysis['compilation_mismatch_list']) - 10} more\n")
            
            # Summary
            f.write("\n4. Summary\n")
            f.write("-" * 10 + "\n")
            
            total_graphdb_datasets = sum(self.graphdb_compilations.values())
            total_lipd_datasets = sum(analysis['total_datasets'] for analysis in self.lipd_analysis.values())
            total_with_compilation = sum(analysis['datasets_with_compilation'] for analysis in self.lipd_analysis.values())
            total_without_compilation = sum(analysis['datasets_without_compilation'] for analysis in self.lipd_analysis.values())
            
            f.write(f"GraphDB total datasets: {total_graphdb_datasets}\n")
            f.write(f"Downloaded total datasets: {total_lipd_datasets}\n")
            f.write(f"Datasets with compilation assignment: {total_with_compilation}\n")
            f.write(f"Datasets without compilation assignment: {total_without_compilation}\n")
            
            if total_lipd_datasets > 0:
                coverage_percent = (total_with_compilation / total_lipd_datasets) * 100
                f.write(f"Compilation assignment coverage: {coverage_percent:.1f}%\n")
        
        print(f"\nReport generated: {report_path}")
        
        # Also generate CSV summary
        self.generate_csv_summary()

    def generate_csv_summary(self):
        """
        Generate CSV summary of the analysis.
        """
        csv_path = self.output_dir / "compilation_summary.csv"
        
        rows = []
        for comp_name in self.graphdb_compilations.keys():
            row = {
                'compilation_name': comp_name,
                'graphdb_datasets': self.graphdb_compilations[comp_name],
                'local_found': comp_name in self.local_compilations,
                'lipd_total_datasets': 0,
                'lipd_with_compilation': 0,
                'lipd_without_compilation': 0,
                'compilation_matches': 0,
                'compilation_mismatches': 0
            }
            
            if comp_name in self.lipd_analysis:
                analysis = self.lipd_analysis[comp_name]
                row.update({
                    'lipd_total_datasets': analysis['total_datasets'],
                    'lipd_with_compilation': analysis['datasets_with_compilation'],
                    'lipd_without_compilation': analysis['datasets_without_compilation'],
                    'compilation_matches': analysis['compilation_matches'],
                    'compilation_mismatches': analysis['compilation_mismatches']
                })
            
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(csv_path, index=False)
        print(f"CSV summary generated: {csv_path}")

    def generate_dataset_comparison_csv(self):
        """Generate a CSV comparing dataset presence and compilation membership across GraphDB and local collections."""
        csv_path = self.output_dir / "dataset_comparison.csv"
        # Build union of dataset names
        dataset_names = set(self.graphdb_dataset_compilations.keys()) | set(self.local_dataset_info.keys())

        with open(csv_path, 'w', newline='') as csvfile:
            fieldnames = [
                'datasetName',
                'inGraphDB',
                'inLocal',
                'collections_dir',
                'collections_lipdfile',
                'collections_graphdb'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for ds in sorted(dataset_names):
                in_graphdb = ds in self.graphdb_dataset_compilations
                in_local = ds in self.local_dataset_info
                dir_comps = sorted(self.local_dataset_info[ds]['dir_comps']) if in_local else []
                lipd_comps = sorted(self.local_dataset_info[ds]['lipd_comps']) if in_local else []
                graphdb_comps = sorted(self.graphdb_dataset_compilations[ds]) if in_graphdb else []

                writer.writerow({
                    'datasetName': ds,
                    'inGraphDB': in_graphdb,
                    'inLocal': in_local,
                    'collections_dir': '|'.join(dir_comps),
                    'collections_lipdfile': '|'.join(lipd_comps),
                    'collections_graphdb': '|'.join(graphdb_comps)
                })
        print(f"Dataset comparison CSV generated: {csv_path}")

    def run_analysis(self, max_compilations=None):
        """
        Run the complete compilation analysis workflow using local LiPD files.
        
        Parameters
        ----------
        max_compilations : int, optional
            Limit analysis to first N compilations (for testing)
        """
        print("Starting LiPDVerse Compilation Analysis (Local Files)...")
        print("=" * 50)
        
        try:
            # Step 1: Query GraphDB for compilations (for comparison)
            print("Querying GraphDB for compilation information...")
            self.execute_sparql_query()
            
            # Step 2: Scan input directory for LiPD files
            local_compilations = self.scan_input_directory()
            
            if not local_compilations:
                print("No LiPD files found in input directory. Exiting.")
                return
            
            # Limit compilations if requested
            if max_compilations:
                original_count = len(local_compilations)
                compilation_items = list(local_compilations.items())[:max_compilations]
                local_compilations = dict(compilation_items)
                print(f"Limited to first {len(local_compilations)} of {original_count} compilations")
            
            # Step 3: Analyze LiPD files for each compilation
            print(f"\nAnalyzing LiPD files for {len(local_compilations)} compilation(s)...")
            for compilation_name, lipd_dir in local_compilations.items():
                self.analyze_lipd_compilation(compilation_name, lipd_dir)
            
            # Step 4: Fetch dataset-compilation mapping from GraphDB
            print("\nFetching dataset-compilation mapping from GraphDB...")
            self.fetch_graphdb_dataset_compilations()
            
            # Step 5: Generate reports
            print("\nGenerating analysis reports...")
            self.generate_report()
            self.generate_dataset_comparison_csv()
            
            print("\n✅ Analysis complete!")
            print(f"Results saved to: {self.output_dir}")
            
        except Exception as e:
            print(f"\n❌ Analysis failed: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Analyze LiPD files for compilation assignments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--input-dir',
        required=True,
        help='Directory containing LiPD files to analyze (can contain subdirectories for different compilations)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='./compilation_analysis',
        help='Directory to store analysis results (default: ./compilation_analysis)'
    )
    
    parser.add_argument(
        '--sparql-endpoint',
        default='https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse-dynamic',
        help='SPARQL endpoint URL for comparison (default: LinkedEarth GraphDB)'
    )
    
    parser.add_argument(
        '--max-compilations',
        type=int,
        help='Limit analysis to first N compilations (for testing)'
    )
    
    args = parser.parse_args()
    
    # Create analyzer and run
    analyzer = CompilationAnalyzer(args.sparql_endpoint, args.input_dir, args.output_dir)
    
    analyzer.run_analysis(max_compilations=args.max_compilations)


if __name__ == "__main__":
    main() 