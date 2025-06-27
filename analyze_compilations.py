#!/usr/bin/env python3
"""
Compilation Analysis Script for LiPDVerse

This script:
1. Queries GraphDB repository to get compilation names and dataset counts
2. Downloads LiPD files for each compilation from LiPDverse
3. Loads LiPD files using PyLiPD and analyzes compilation assignments
4. Generates reports on compilation consistency and coverage

Usage:
    python analyze_compilations.py [--output-dir OUTPUT_DIR] [--sparql-endpoint ENDPOINT]
"""

import os
import sys
import argparse
import requests
import zipfile
import tempfile
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict, Counter
import csv

from pylipd.lipd import LiPD


class CompilationAnalyzer:
    def __init__(self, sparql_endpoint, output_dir):
        self.sparql_endpoint = sparql_endpoint
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Results storage
        self.graphdb_compilations = {}
        self.downloaded_compilations = {}
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

    def find_download_link(self, compilation_name):
        """
        Find the download link for a specific compilation from LiPDverse.
        Uses a multi-step search process:
        1. First check the main page: https://lipdverse.org/[compilation]/current_version/
        2. If not found, check the sidebar: https://lipdverse.org/[compilation]/current_version/projectSidebar.html
        
        Parameters
        ----------
        compilation_name : str
            Name of the compilation
            
        Returns
        -------
        str or None
            Download URL if found, None otherwise
        """
        base_url = f"https://lipdverse.org/{compilation_name}/current_version/"
        main_url = base_url
        sidebar_url = f"{base_url}projectSidebar.html"
        
        def search_for_download_links(url, soup):
            """Helper function to search for download links in a BeautifulSoup object"""
            # Look for "Download all LiPD files" link
            for link in soup.find_all('a', href=True):
                link_text = link.get_text(strip=True).lower()
                if 'download all lipd files' in link_text or 'download all' in link_text:
                    href = link['href']
                    if href.startswith('http'):
                        return href
                    else:
                        return urljoin(base_url, href)
            
            # Fallback: look for .zip files
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.endswith('.zip') and ('lipd' in href.lower() or 'all' in href.lower()):
                    if href.startswith('http'):
                        return href
                    else:
                        return urljoin(base_url, href)
            
            return None
        
        # Step 1: Try main page
        print(f"Looking for download link on main page: {main_url}")
        try:
            response = requests.get(main_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            download_url = search_for_download_links(main_url, soup)
            
            if download_url:
                print(f"  Found download link on main page: {download_url}")
                return download_url
            else:
                print(f"  No download link found on main page")
                
        except Exception as e:
            print(f"  Error accessing main page for {compilation_name}: {e}")
        
        # Step 2: Try sidebar page
        print(f"Looking for download link on sidebar: {sidebar_url}")
        try:
            response = requests.get(sidebar_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            download_url = search_for_download_links(sidebar_url, soup)
            
            if download_url:
                print(f"  Found download link on sidebar: {download_url}")
                return download_url
            else:
                print(f"  No download link found on sidebar")
                
        except Exception as e:
            print(f"  Error accessing sidebar for {compilation_name}: {e}")
        
        print(f"  No download link found for {compilation_name}")
        return None

    def download_compilation(self, compilation_name, download_url):
        """
        Download and extract LiPD files for a compilation.
        
        Parameters
        ----------
        compilation_name : str
            Name of the compilation
        download_url : str
            URL to download the ZIP file from
            
        Returns
        -------
        str or None
            Path to extracted LiPD files directory
        """
        compilation_dir = self.output_dir / "compilations" / compilation_name
        compilation_dir.mkdir(parents=True, exist_ok=True)
        
        zip_path = compilation_dir / f"{compilation_name}.zip"
        extract_dir = compilation_dir / "lipd_files"
        
        if zip_path.exists():
            print(f"Zip file already exists for {compilation_name}: {zip_path}. Skipping download.")
        else:
            print(f"Downloading {compilation_name} from: {download_url}")
            try:
                # Download ZIP file
                with requests.get(download_url, stream=True) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get('content-length', 0))
                    
                    with open(zip_path, 'wb') as f:
                        downloaded = 0
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total_size > 0:
                                    percent = (downloaded / total_size) * 100
                                    print(f"\r  Progress: {percent:.1f}%", end='')
                print(f"\n  Download completed: {zip_path}")
            except Exception as e:
                print(f"  Error downloading {compilation_name}: {e}")
                return None
        
        # Extract ZIP file (whether just downloaded or existing)
        try:
            extract_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Find the actual LiPD files directory
            lipd_files = list(extract_dir.rglob("*.lpd"))
            if lipd_files:
                # Find the common directory containing most LiPD files
                directories = [f.parent for f in lipd_files]
                most_common_dir = max(set(directories), key=directories.count)
                print(f"  Extracted {len(lipd_files)} LiPD files to: {most_common_dir}")
                return str(most_common_dir)
            else:
                print(f"  Warning: No LiPD files found in {extract_dir}")
                return None
        except Exception as e:
            print(f"  Error extracting {compilation_name}: {e}")
            return None

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
            
            # Download Results
            f.write("2. Download Results\n")
            f.write("-" * 20 + "\n")
            f.write(f"Successfully downloaded: {len(self.downloaded_compilations)} compilations\n\n")
            
            for comp_name in sorted(self.downloaded_compilations.keys()):
                f.write(f"  ✓ {comp_name}\n")
            
            failed_downloads = set(self.graphdb_compilations.keys()) - set(self.downloaded_compilations.keys())
            if failed_downloads:
                f.write(f"\nFailed downloads: {len(failed_downloads)} compilations\n")
                for comp_name in sorted(failed_downloads):
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
                'download_success': comp_name in self.downloaded_compilations,
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
        Run the complete compilation analysis workflow.
        
        Parameters
        ----------
        max_compilations : int, optional
            Limit analysis to first N compilations (for testing)
        """
        print("Starting LiPDVerse Compilation Analysis...")
        print("=" * 50)
        
        try:
            # Step 1: Query GraphDB for compilations
            compilations = self.execute_sparql_query()
            
            if not compilations:
                print("No compilations found in GraphDB. Exiting.")
                return
            
            # Limit compilations if requested
            if max_compilations:
                original_count = len(compilations)
                compilation_items = list(compilations.items())[:max_compilations]
                compilations = dict(compilation_items)
                print(f"Limited to first {len(compilations)} of {original_count} compilations")
            
            # Step 2: Download LiPD files for each compilation
            print(f"\nDownloading LiPD files for {len(compilations)} compilations...")
            for compilation_name in compilations.keys():
                download_url = self.find_download_link(compilation_name)
                
                if download_url:
                    lipd_dir = self.download_compilation(compilation_name, download_url)
                    if lipd_dir:
                        self.downloaded_compilations[compilation_name] = lipd_dir
                else:
                    print(f"Could not find download link for: {compilation_name}")
            
            # Step 3: Analyze LiPD files for each downloaded compilation
            print(f"\nAnalyzing LiPD files for {len(self.downloaded_compilations)} compilations...")
            for compilation_name, lipd_dir in self.downloaded_compilations.items():
                self.analyze_lipd_compilation(compilation_name, lipd_dir)
            
            # Step 4: Fetch dataset-compilation mapping from GraphDB
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
        description="Analyze LiPDVerse compilations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--output-dir',
        default='./compilation_analysis',
        help='Directory to store analysis results (default: ./compilation_analysis)'
    )
    
    parser.add_argument(
        '--sparql-endpoint',
        default='https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse-dynamic',
        help='SPARQL endpoint URL (default: LinkedEarth GraphDB)'
    )
    
    parser.add_argument(
        '--max-compilations',
        type=int,
        help='Limit analysis to first N compilations (for testing)'
    )
    
    args = parser.parse_args()
    
    # Create analyzer and run
    analyzer = CompilationAnalyzer(args.sparql_endpoint, args.output_dir)
    
    analyzer.run_analysis(max_compilations=args.max_compilations)


if __name__ == "__main__":
    main() 