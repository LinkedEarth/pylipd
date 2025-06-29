#!/usr/bin/env python3
"""
Upload data to GraphDB

This script:
1. Connects to a GraphDB instance
2. Deletes all existing graphs (except the default graph)
3. Imports a .nq.zip file with target graphs set to "from data"

Usage:
    python upload_to_graphdb.py --endpoint ENDPOINT --nq-zip-file FILE [--username USER] [--password PASS]
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
    def __init__(self, endpoint_url, username=None, password=None):
        """
        Initialize GraphDB uploader.
        
        Parameters
        ----------
        endpoint_url : str
            GraphDB repository endpoint URL (e.g., http://localhost:7200/repositories/myrepo)
        username : str, optional
            Username for authentication
        password : str, optional
            Password for authentication
        """
        self.endpoint_url = endpoint_url.rstrip('/')
        self.base_url = '/'.join(endpoint_url.split('/')[:-2])  # Remove /repositories/reponame
        self.repo_name = endpoint_url.split('/')[-1]
        self.username = username
        self.password = password
        
        # Setup authentication
        self.auth = None
        if username and password:
            self.auth = (username, password)
        
        # Upload statistics
        self.upload_stats = {
            'graphs_deleted': 0,
            'import_successful': False,
            'import_time_seconds': 0,
            'errors': []
        }
        
        print(f"GraphDB Uploader initialized:")
        print(f"  Base URL: {self.base_url}")
        print(f"  Repository: {self.repo_name}")
        print(f"  Authentication: {'Yes' if self.auth else 'No'}")

    def test_connection(self):
        """Test connection to GraphDB."""
        print("Testing connection to GraphDB...")
        
        try:
            # Test basic connectivity
            test_url = f"{self.base_url}/rest/repositories"
            response = requests.get(test_url, auth=self.auth, timeout=10)
            response.raise_for_status()
            
            # Check if our repository exists
            repositories = response.json()
            repo_exists = any(repo['id'] == self.repo_name for repo in repositories)
            
            if repo_exists:
                print(f"✓ Connected to GraphDB successfully")
                print(f"✓ Repository '{self.repo_name}' found")
                return True
            else:
                available_repos = [repo['id'] for repo in repositories]
                raise Exception(f"Repository '{self.repo_name}' not found. Available repositories: {available_repos}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to GraphDB: {e}")

    def get_existing_graphs(self):
        """Get list of existing named graphs."""
        print("Retrieving existing graphs...")
        
        try:
            # SPARQL query to get all named graphs
            query = """
            SELECT DISTINCT ?graph WHERE {
                GRAPH ?graph { ?s ?p ?o }
            }
            ORDER BY ?graph
            """
            
            query_url = f"{self.endpoint_url}"
            response = requests.post(
                query_url,
                data={'query': query},
                headers={'Accept': 'application/sparql-results+json'},
                auth=self.auth,
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            graphs = [binding['graph']['value'] for binding in results['results']['bindings']]
            
            # Filter out the default graph (usually represented as empty string or special URI)
            named_graphs = [g for g in graphs if g and not g.endswith('#default')]
            
            print(f"Found {len(named_graphs)} named graphs:")
            for graph in named_graphs[:10]:  # Show first 10
                print(f"  - {graph}")
            if len(named_graphs) > 10:
                print(f"  ... and {len(named_graphs) - 10} more")
            
            return named_graphs
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve graphs: {e}")

    def delete_graph(self, graph_uri):
        """Delete a specific named graph."""
        try:
            # SPARQL UPDATE to delete the graph
            update_query = f"DROP GRAPH <{graph_uri}>"
            
            update_url = f"{self.endpoint_url}/statements"
            response = requests.post(
                update_url,
                data={'update': update_query},
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                auth=self.auth,
                timeout=60
            )
            response.raise_for_status()
            
            return True
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to delete graph {graph_uri}: {e}"
            self.upload_stats['errors'].append(error_msg)
            print(f"  ✗ {error_msg}")
            return False

    def delete_all_graphs(self, exclude_default=True):
        """Delete all named graphs except the default graph."""
        print("Deleting existing graphs...")
        
        graphs = self.get_existing_graphs()
        
        if not graphs:
            print("No named graphs to delete")
            return True
        
        print(f"Deleting {len(graphs)} graphs...")
        
        deleted_count = 0
        for graph_uri in graphs:
            print(f"  Deleting: {graph_uri}")
            if self.delete_graph(graph_uri):
                deleted_count += 1
                print(f"  ✓ Deleted: {graph_uri}")
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.1)
        
        self.upload_stats['graphs_deleted'] = deleted_count
        
        if deleted_count == len(graphs):
            print(f"✓ Successfully deleted {deleted_count} graphs")
            return True
        else:
            print(f"⚠ Deleted {deleted_count} out of {len(graphs)} graphs")
            return False

    def import_nq_zip(self, nq_zip_file):
        """
        Import a .nq.zip file into GraphDB with target graphs set to "from data".
        
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
            # GraphDB import endpoint
            import_url = f"{self.base_url}/rest/data/import/upload/{self.repo_name}/text"
            
            # Prepare the file for upload
            with open(nq_zip_path, 'rb') as f:
                files = {
                    'file': (nq_zip_path.name, f, 'application/zip')
                }
                
                # Import settings - target graphs from data
                data = {
                    'type': 'text',
                    'format': 'application/x-gzip',  # GraphDB expects this for .nq.zip
                    'context': '',  # Empty means use graphs from data
                    'forceSerial': 'false',
                    'stopOnError': 'true',
                    'parserSettings': json.dumps({
                        'preserveBNodeIds': False,
                        'failOnUnknownDataTypes': False,
                        'verifyDataTypeValues': False,
                        'normalizeDataTypeValues': False,
                        'failOnUnknownLanguageTags': False,
                        'verifyLanguageTags': True,
                        'normalizeLanguageTags': False
                    })
                }
                
                print("Uploading file to GraphDB...")
                start_time = time.time()
                
                response = requests.post(
                    import_url,
                    files=files,
                    data=data,
                    auth=self.auth,
                    timeout=1800  # 30 minute timeout for large files
                )
                response.raise_for_status()
                
                end_time = time.time()
                self.upload_stats['import_time_seconds'] = end_time - start_time
                
                # Check response
                if response.status_code == 202:
                    print("✓ File uploaded successfully")
                    print(f"✓ Import completed in {self.upload_stats['import_time_seconds']:.1f} seconds")
                    self.upload_stats['import_successful'] = True
                    return True
                else:
                    raise Exception(f"Import failed with status code: {response.status_code}")
                    
        except requests.exceptions.RequestException as e:
            error_msg = f"Import failed: {e}"
            self.upload_stats['errors'].append(error_msg)
            raise Exception(error_msg)

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
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            triple_count = int(results['results']['bindings'][0]['count']['value'])
            
            print(f"✓ Import verified: {triple_count:,} triples in repository")
            
            # Get graph count
            graphs = self.get_existing_graphs()
            print(f"✓ {len(graphs)} named graphs created")
            
            return True
            
        except Exception as e:
            print(f"⚠ Could not verify import: {e}")
            return False

    def upload_to_graphdb(self, nq_zip_file):
        """
        Complete upload process: test connection, delete graphs, import data.
        
        Parameters
        ----------
        nq_zip_file : str or Path
            Path to the .nq.zip file to upload
        """
        print("Starting GraphDB Upload Process")
        print("=" * 35)
        
        try:
            # Step 1: Test connection
            self.test_connection()
            
            # Step 2: Delete existing graphs
            self.delete_all_graphs()
            
            # Step 3: Import new data
            self.import_nq_zip(nq_zip_file)
            
            # Step 4: Verify import
            self.verify_import()
            
            print("\n" + "=" * 35)
            print("✅ GraphDB Upload Complete!")
            print(f"Graphs deleted: {self.upload_stats['graphs_deleted']}")
            print(f"Import time: {self.upload_stats['import_time_seconds']:.1f} seconds")
            print(f"Repository: {self.endpoint_url}")
            
        except Exception as e:
            self.upload_stats['errors'].append(str(e))
            print(f"\n❌ Upload failed: {e}")
            raise

    def generate_report(self):
        """Generate an upload report."""
        report_data = {
            'endpoint': self.endpoint_url,
            'repository': self.repo_name,
            'graphs_deleted': self.upload_stats['graphs_deleted'],
            'import_successful': self.upload_stats['import_successful'],
            'import_time_seconds': self.upload_stats['import_time_seconds'],
            'errors': self.upload_stats['errors']
        }
        
        print(f"Upload Report:")
        print(f"  Endpoint: {report_data['endpoint']}")
        print(f"  Graphs deleted: {report_data['graphs_deleted']}")
        print(f"  Import successful: {report_data['import_successful']}")
        print(f"  Import time: {report_data['import_time_seconds']:.1f} seconds")
        if report_data['errors']:
            print(f"  Errors: {len(report_data['errors'])}")


def main():
    parser = argparse.ArgumentParser(
        description="Upload .nq.zip file to GraphDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload to local GraphDB instance
  python upload_to_graphdb.py --endpoint http://localhost:7200/repositories/myrepo --nq-zip-file graphdb_output/all-lipd.nq.zip

  # Upload with authentication
  python upload_to_graphdb.py --endpoint https://graphdb.example.com/repositories/lipd --nq-zip-file data.nq.zip --username admin --password secret

  # Upload to remote GraphDB instance
  python upload_to_graphdb.py --endpoint https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse-dynamic --nq-zip-file all-lipd.nq.zip
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
        '--username',
        type=str,
        help='Username for GraphDB authentication'
    )
    
    parser.add_argument(
        '--password',
        type=str,
        help='Password for GraphDB authentication'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test connection and show what would be deleted without actually doing it'
    )
    
    args = parser.parse_args()
    
    # Create and run the uploader
    uploader = GraphDBUploader(
        endpoint_url=args.endpoint,
        username=args.username,
        password=args.password
    )
    
    try:
        if args.dry_run:
            print("DRY RUN MODE - No changes will be made")
            uploader.test_connection()
            graphs = uploader.get_existing_graphs()
            print(f"Would delete {len(graphs)} graphs and import {args.nq_zip_file}")
        else:
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