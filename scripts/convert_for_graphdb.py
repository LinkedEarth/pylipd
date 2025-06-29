#!/usr/bin/env python3
"""
Convert LiPD files to GraphDB-ready format

This script:
1. Takes a directory of LiPD files (e.g., from download_compilations.py or preprocess_compilations.py)
2. Converts them to RDF (.nq format) using PyLiPD
3. Creates a compressed .nq.zip file for GraphDB import

Usage:
    python convert_for_graphdb.py --input-dir INPUT_DIR [--output-dir OUTPUT_DIR] [--nq-filename FILENAME]
"""

import os
import sys
import argparse
import zipfile
from pathlib import Path
from tqdm import tqdm

# Add the project root to the path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from pylipd.lipd import LiPD
except ImportError as e:
    print(f"Error importing PyLiPD: {e}")
    print("Please ensure PyLiPD is installed: pip install pylipd")
    sys.exit(1)


class GraphDBConverter:
    def __init__(self, input_dir, output_dir="graphdb_output"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Conversion statistics
        self.conversion_stats = {
            'input_files_found': 0,
            'conversion_successful': False,
            'output_nq_size': 0,
            'output_zip_size': 0,
            'errors': []
        }

    def find_lipd_files(self):
        """Find all LiPD files in the input directory and subdirectories."""
        print(f"Searching for LiPD files in: {self.input_dir}")
        
        if not self.input_dir.exists():
            raise ValueError(f"Input directory does not exist: {self.input_dir}")
        
        # Find all .lpd files recursively
        lipd_files = list(self.input_dir.rglob("*.lpd"))
        
        if not lipd_files:
            raise ValueError(f"No LiPD files found in: {self.input_dir}")
        
        print(f"Found {len(lipd_files)} LiPD files")
        
        # Group files by directory for reporting
        directories = {}
        for file_path in lipd_files:
            dir_name = file_path.parent.name
            if dir_name not in directories:
                directories[dir_name] = []
            directories[dir_name].append(file_path.name)
        
        print("Files by directory:")
        for dir_name, files in directories.items():
            print(f"  {dir_name}: {len(files)} files")
        
        self.conversion_stats['input_files_found'] = len(lipd_files)
        return lipd_files

    def convert_to_rdf(self, lipd_files, output_nq_file):
        """
        Convert LiPD files to RDF using PyLiPD.
        
        Parameters
        ----------
        lipd_files : list of Path
            List of LiPD file paths
        output_nq_file : Path
            Output .nq file path
        """
        print(f"Converting {len(lipd_files)} LiPD files to RDF...")
        print(f"Output file: {output_nq_file}")
        
        try:
            # Initialize LiPD
            L = LiPD()
            
            # For PyLiPD's convert_lipd_dir_to_rdf, we need a directory
            # So we'll create a temporary directory with symlinks or use the existing structure
            
            # Find the common parent directory or use input_dir
            if len(set(f.parent for f in lipd_files)) == 1:
                # All files are in the same directory
                lipd_dir = lipd_files[0].parent
            else:
                # Files are in multiple directories, use the input directory
                lipd_dir = self.input_dir
            
            print(f"Using LiPD directory: {lipd_dir}")
            
            # Convert LiPD files to RDF
            L.convert_lipd_dir_to_rdf(
                str(lipd_dir),
                str(output_nq_file),
                parallel=True,
                standardize=True,
                add_labels=False
            )
            
            # Check if file was created and get size
            if output_nq_file.exists():
                file_size = output_nq_file.stat().st_size
                self.conversion_stats['output_nq_size'] = file_size
                print(f"✓ RDF conversion completed: {output_nq_file}")
                print(f"  File size: {file_size:,} bytes ({file_size / (1024*1024):.1f} MB)")
                return True
            else:
                raise Exception("Output .nq file was not created")
                
        except Exception as e:
            error_msg = f"RDF conversion failed: {e}"
            print(f"✗ {error_msg}")
            self.conversion_stats['errors'].append(error_msg)
            return False

    def create_zip_file(self, nq_file, zip_file):
        """
        Create a compressed .nq.zip file for GraphDB import.
        
        Parameters
        ----------
        nq_file : Path
            Input .nq file path
        zip_file : Path
            Output .nq.zip file path
        """
        print(f"Creating compressed file: {zip_file}")
        
        try:
            with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                # Add the .nq file to the zip with just its filename (no path)
                zipf.write(nq_file, nq_file.name)
            
            # Check if zip file was created and get size
            if zip_file.exists():
                zip_size = zip_file.stat().st_size
                nq_size = nq_file.stat().st_size
                compression_ratio = (1 - zip_size / nq_size) * 100
                
                self.conversion_stats['output_zip_size'] = zip_size
                
                print(f"✓ Compressed file created: {zip_file}")
                print(f"  Original size: {nq_size:,} bytes ({nq_size / (1024*1024):.1f} MB)")
                print(f"  Compressed size: {zip_size:,} bytes ({zip_size / (1024*1024):.1f} MB)")
                print(f"  Compression ratio: {compression_ratio:.1f}%")
                return True
            else:
                raise Exception("Output .nq.zip file was not created")
                
        except Exception as e:
            error_msg = f"ZIP creation failed: {e}"
            print(f"✗ {error_msg}")
            self.conversion_stats['errors'].append(error_msg)
            return False

    def convert_for_graphdb(self, nq_filename="all-lipd.nq"):
        """
        Main conversion process: LiPD files -> .nq -> .nq.zip
        
        Parameters
        ----------
        nq_filename : str
            Name for the output .nq file
        """
        print("Starting GraphDB Conversion Process")
        print("=" * 40)
        
        try:
            # Step 1: Find LiPD files
            lipd_files = self.find_lipd_files()
            
            # Step 2: Convert to RDF (.nq format)
            nq_file = self.output_dir / nq_filename
            conversion_success = self.convert_to_rdf(lipd_files, nq_file)
            
            if not conversion_success:
                raise Exception("RDF conversion failed")
            
            # Step 3: Create compressed .nq.zip file
            zip_filename = nq_filename + ".zip"
            zip_file = self.output_dir / zip_filename
            zip_success = self.create_zip_file(nq_file, zip_file)
            
            if not zip_success:
                raise Exception("ZIP creation failed")
            
            self.conversion_stats['conversion_successful'] = True
            
            print("\n" + "=" * 40)
            print("✅ GraphDB Conversion Complete!")
            print(f"Input files: {self.conversion_stats['input_files_found']} LiPD files")
            print(f"Output files:")
            print(f"  - RDF file: {nq_file}")
            print(f"  - Compressed: {zip_file}")
            print(f"Files ready for GraphDB import!")
            
        except Exception as e:
            self.conversion_stats['errors'].append(str(e))
            print(f"\n❌ Conversion failed: {e}")
            raise

    def generate_report(self):
        """Generate a conversion report."""
        report_path = self.output_dir / "conversion_report.txt"
        
        with open(report_path, 'w') as f:
            f.write("GraphDB Conversion Report\n")
            f.write("=" * 25 + "\n\n")
            
            f.write(f"Input directory: {self.input_dir}\n")
            f.write(f"Output directory: {self.output_dir}\n")
            f.write(f"LiPD files processed: {self.conversion_stats['input_files_found']}\n")
            f.write(f"Conversion successful: {self.conversion_stats['conversion_successful']}\n")
            
            if self.conversion_stats['output_nq_size'] > 0:
                f.write(f"RDF file size: {self.conversion_stats['output_nq_size']:,} bytes\n")
            
            if self.conversion_stats['output_zip_size'] > 0:
                f.write(f"Compressed file size: {self.conversion_stats['output_zip_size']:,} bytes\n")
            
            if self.conversion_stats['errors']:
                f.write(f"\nErrors encountered: {len(self.conversion_stats['errors'])}\n")
                for error in self.conversion_stats['errors']:
                    f.write(f"  - {error}\n")
        
        print(f"Report generated: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert LiPD files to GraphDB-ready format (.nq and .nq.zip)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert files from download_compilations.py output
  python convert_for_graphdb.py --input-dir lipd_compilations

  # Convert files from preprocess_compilations.py output
  python convert_for_graphdb.py --input-dir lipd_statistics_updated_sparql/updated_files

  # Specify custom output directory and filename
  python convert_for_graphdb.py --input-dir my_lipd_files --output-dir graphdb_ready --nq-filename my-data.nq
        """
    )
    
    parser.add_argument(
        '--input-dir',
        type=str,
        required=True,
        help='Directory containing LiPD files to convert'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='graphdb_output',
        help='Output directory for .nq and .nq.zip files (default: graphdb_output)'
    )
    
    parser.add_argument(
        '--nq-filename',
        type=str,
        default='all-lipd.nq',
        help='Name for the output .nq file (default: all-lipd.nq)'
    )
    
    args = parser.parse_args()
    
    # Create and run the converter
    converter = GraphDBConverter(
        input_dir=args.input_dir,
        output_dir=args.output_dir
    )
    
    try:
        converter.convert_for_graphdb(args.nq_filename)
        converter.generate_report()
    except KeyboardInterrupt:
        print("\nConversion process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        converter.generate_report()
        sys.exit(1)


if __name__ == "__main__":
    main() 