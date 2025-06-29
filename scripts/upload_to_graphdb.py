#!/usr/bin/env python3
"""
Upload data to GraphDB

This script:
1. Connects to a GraphDB instance
2. Clears the entire repository
3. Imports all TTL files from ontology/*.ttl to the default graph
4. Imports a .nq.zip file with target graphs set to "from data"

Usage:
    python upload_to_graphdb.py --endpoint ENDPOINT --nq-zip-file FILE [--ontology-dir ONTOLOGY_DIR] [--username USER] [--password PASS]
"""

import os
import sys
import argparse
import requests
import time
from pathlib import Path
from urllib.parse import urljoin
import json


class GraphDBUploader:
    def __init__(self, endpoint_url, ontology_dir="ontology", username=None, password=None):
        """
        Initialize GraphDB uploader.
        
        Parameters
        ----------
        endpoint_url : str
            GraphDB repository endpoint URL (e.g., http://localhost:7200/repositories/myrepo)
        ontology_dir : str
            Directory containing TTL ontology files
        username : str, optional
            Username for authentication
        password : str, optional
            Password for authentication
        """
        self.endpoint_url = endpoint_url.rstrip('/')
        self.base_url = '/'.join(endpoint_url.split('/')[:-2])  # Remove /repositories/reponame
        self.repo_name = endpoint_url.split('/')[-1]
        self.ontology_dir = Path(ontology_dir)
        self.username = username
        self.password = password
        
        # Setup authentication
        self.auth = None
        if username and password:
            self.auth = (username, password)
        
        # Upload statistics
        self.upload_stats = {
            'repository_cleared': False,
            'ontology_files_imported': 0,
            'data_import_successful': False,
            'total_time_seconds': 0,
            'errors': []
        }
        
        print(f"GraphDB Uploader initialized:")
        print(f"  Base URL: {self.base_url}")
        print(f"  Repository: {self.repo_name}")
        print(f"  Ontology directory: {self.ontology_dir}")
        print(f"  Authentication: {'Yes' if self.auth else 'No'}")

    def test_connection(self):
        """Test connection to GraphDB."""
        print("Testing connection to GraphDB...")
        
        try:
            # Test basic connectivity with REST API
            test_url = f"{self.base_url}/rest/repositories"
            response = requests.get(test_url, auth=self.auth, timeout=10)
            response.raise_for_status()
            
            # Check if our repository exists
            repositories = response.json()
            repo_exists = any(repo['id'] == self.repo_name for repo in repositories)
            
            if repo_exists:
                print(f"✓ Connected to GraphDB successfully")
                print(f"✓ Repository '{self.repo_name}' found")
                
                # Test SPARQL endpoint specifically
                try:
                    test_query = "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
                    sparql_response = requests.post(
                        f"{self.endpoint_url}",
                        data={'query': test_query},
                        headers={'Accept': 'application/sparql-results+json'},
                        auth=self.auth,
                        timeout=10
                    )
                    sparql_response.raise_for_status()
                    print(f"✓ SPARQL endpoint working")
                except Exception as e:
                    print(f"⚠ SPARQL endpoint test failed: {e}")
                
                return True
            else:
                available_repos = [repo['id'] for repo in repositories]
                raise Exception(f"Repository '{self.repo_name}' not found. Available repositories: {available_repos}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to GraphDB: {e}")

    def clear_repository(self):
        """Clear the entire repository using SPARQL."""
        print("Clearing repository...")
        
        try:
            # Use SPARQL UPDATE to clear all data
            clear_query = "CLEAR ALL"
            
            response = requests.post(
                f"{self.endpoint_url}/statements",
                data={'update': clear_query},
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                auth=self.auth,
                timeout=300  # 5 minute timeout
            )
            response.raise_for_status()
            
            print("✓ Repository cleared successfully")
            self.upload_stats['repository_cleared'] = True
            return True
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to clear repository: {e}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" - Response: {e.response.text}"
            print(f"✗ {error_msg}")
            self.upload_stats['errors'].append(error_msg)
            return False

    def import_ontology_files(self):
        """Import all TTL files from the ontology directory to the default graph."""
        print("Importing ontology files...")
        
        if not self.ontology_dir.exists():
            print(f"⚠ Ontology directory not found: {self.ontology_dir}")
            return True  # Not an error, just skip
        
        # Find all TTL files
        ttl_files = list(self.ontology_dir.glob("*.ttl"))
        
        if not ttl_files:
            print(f"⚠ No TTL files found in: {self.ontology_dir}")
            return True  # Not an error, just skip
        
        print(f"Found {len(ttl_files)} TTL files to import:")
        for ttl_file in ttl_files:
            print(f"  - {ttl_file.name}")
        
        imported_count = 0
        
        for ttl_file in ttl_files:
            try:
                print(f"  Importing {ttl_file.name}...")
                
                # Read TTL file content
                with open(ttl_file, 'r', encoding='utf-8') as f:
                    ttl_content = f.read()
                
                # Import using SPARQL UPDATE with INSERT DATA
                response = requests.post(
                    f"{self.endpoint_url}/statements",
                    data=ttl_content,
                    headers={'Content-Type': 'text/turtle'},
                    auth=self.auth,
                    timeout=300
                )
                response.raise_for_status()
                
                print(f"  ✓ Imported {ttl_file.name}")
                imported_count += 1
                
            except Exception as e:
                error_msg = f"Failed to import {ttl_file.name}: {e}"
                if hasattr(e, 'response') and e.response is not None:
                    error_msg += f" - Response: {e.response.text}"
                print(f"  ✗ {error_msg}")
                self.upload_stats['errors'].append(error_msg)
        
        self.upload_stats['ontology_files_imported'] = imported_count
        
        if imported_count > 0:
            print(f"✓ Successfully imported {imported_count} ontology files")
            return True
        else:
            print("⚠ No ontology files were imported")
            return len(ttl_files) == 0  # Success if there were no files to import

    def import_nq_zip(self, nq_zip_file):
        """
        Import a .nq.zip file into GraphDB directly (without extracting).
        GraphDB will handle the extraction and import automatically.
        
        Parameters
        ----------
        nq_zip_file : str or Path
            Path to the .nq.zip file to import
        """
        nq_zip_path = Path(nq_zip_file)
        
        if not nq_zip_path.exists():
            raise Exception(f"File not found: {nq_zip_file}")
        
        print(f"Importing {nq_zip_path.name} into GraphDB...")
        print(f"File size: {nq_zip_path.stat().st_size:,} bytes ({nq_zip_path.stat().st_size / (1024*1024):.1f} MB)")
        
        try:
            # Import the .nq.zip file directly (GraphDB handles the extraction)
            start_time = time.time()
            
            with open(nq_zip_path, 'rb') as f:
                response = requests.post(
                    f"{self.endpoint_url}/statements",
                    data=f.read(),
                    headers={'Content-Type': 'application/zip'},
                    auth=self.auth,
                    timeout=1800  # 30 minute timeout for large files
                )
                response.raise_for_status()
            
            end_time = time.time()
            import_time = end_time - start_time
            
            print(f"✓ Data import completed in {import_time:.1f} seconds")
            self.upload_stats['data_import_successful'] = True
            return True
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Data import failed: {e}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" - Response: {e.response.text}"
            print(f"✗ {error_msg}")
            self.upload_stats['errors'].append(error_msg)
            return False

    def verify_import(self):
        """Verify that data was imported successfully."""
        print("Verifying import...")
        
        try:
            # Count total triples
            count_query = "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
            
            query_url = f"{self.endpoint_url}"
            response = requests.post(
                query_url,
                data={'query': count_query},
                headers={'Accept': 'application/sparql-results+json'},
                auth=self.auth,
                timeout=60  # Increased timeout for verification
            )
            response.raise_for_status()
            
            results = response.json()
            triple_count = int(results['results']['bindings'][0]['count']['value'])
            
            print(f"✓ Import verified: {triple_count:,} triples in repository")
            return True
            
        except Exception as e:
            print(f"⚠ Could not verify import: {e}")
            return False

    def upload_to_graphdb(self, nq_zip_file):
        """
        Complete upload process: clear repository, import ontology, import data.
        
        Parameters
        ----------
        nq_zip_file : str or Path
            Path to the .nq.zip file to upload
        """
        print("Starting GraphDB Upload Process")
        print("=" * 35)
        
        start_time = time.time()
        
        try:
            # Step 1: Test connection
            self.test_connection()
            
            # Step 2: Clear repository
            self.clear_repository()
            
            # Step 3: Import ontology files
            self.import_ontology_files()
            
            # Step 4: Import data
            self.import_nq_zip(nq_zip_file)
            
            # Step 5: Verify import
            self.verify_import()
            
            end_time = time.time()
            self.upload_stats['total_time_seconds'] = end_time - start_time
            
            print("\n" + "=" * 35)
            print("✅ GraphDB Upload Complete!")
            print(f"Repository cleared: {self.upload_stats['repository_cleared']}")
            print(f"Ontology files imported: {self.upload_stats['ontology_files_imported']}")
            print(f"Data import successful: {self.upload_stats['data_import_successful']}")
            print(f"Total time: {self.upload_stats['total_time_seconds']:.1f} seconds")
            print(f"Repository: {self.endpoint_url}")
            
        except Exception as e:
            self.upload_stats['errors'].append(str(e))
            print(f"\n❌ Upload failed: {e}")
            raise

    def generate_report(self):
        """Generate an upload report."""
        print(f"Upload Report:")
        print(f"  Endpoint: {self.endpoint_url}")
        print(f"  Repository cleared: {self.upload_stats['repository_cleared']}")
        print(f"  Ontology files imported: {self.upload_stats['ontology_files_imported']}")
        print(f"  Data import successful: {self.upload_stats['data_import_successful']}")
        print(f"  Total time: {self.upload_stats['total_time_seconds']:.1f} seconds")
        if self.upload_stats['errors']:
            print(f"  Errors: {len(self.upload_stats['errors'])}")
            for error in self.upload_stats['errors']:
                print(f"    - {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Upload data to GraphDB (clear repository, import ontology, import data)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload to local GraphDB instance
  python upload_to_graphdb.py --endpoint http://localhost:7200/repositories/myrepo --nq-zip-file graphdb_output/all-lipd.nq.zip

  # Upload with custom ontology directory
  python upload_to_graphdb.py --endpoint http://localhost:7200/repositories/myrepo --nq-zip-file data.nq.zip --ontology-dir my_ontology

  # Upload with authentication
  python upload_to_graphdb.py --endpoint https://graphdb.example.com/repositories/lipd --nq-zip-file data.nq.zip --username admin --password secret
        """
    )
    
    parser.add_argument(
        '--endpoint',
        type=str,
        required=True,
        help='GraphDB repository endpoint URL (e.g., http://localhost:7200/repositories/myrepo)'
    )
    
    parser.add_argument(
        '--nq-zip-file',
        type=str,
        required=True,
        help='Path to the .nq.zip file to upload'
    )
    
    parser.add_argument(
        '--ontology-dir',
        type=str,
        default='ontology',
        help='Directory containing TTL ontology files (default: ontology)'
    )
    
    parser.add_argument(
        '--username',
        type=str,
        help='Username for GraphDB authentication'
    )
    
    parser.add_argument(
        '--password',
        type=str,
        help='Password for GraphDB authentication'
    )
    
    args = parser.parse_args()
    
    # Create and run the uploader
    uploader = GraphDBUploader(
        endpoint_url=args.endpoint,
        ontology_dir=args.ontology_dir,
        username=args.username,
        password=args.password
    )
    
    try:
        uploader.upload_to_graphdb(args.nq_zip_file)
        uploader.generate_report()
            
    except KeyboardInterrupt:
        print("\nUpload process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        uploader.generate_report()
        sys.exit(1)


if __name__ == "__main__":
    main() 