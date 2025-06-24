#!/usr/bin/env python3
"""
Download all LiPD files from LiPDverse and convert to RDF (.nq format)

This script:
1. Downloads the latest LiPD files from https://lipdverse.org/lipdverse/current_version/projectSidebar.html
2. Extracts them to a local directory
3. Converts all LiPD files to a single RDF .nq file using PyLiPD

Usage:
    python download_and_convert_lipdverse.py [--output-dir OUTPUT_DIR] [--nq-filename NQ_FILENAME]
"""

import os
import sys
import argparse
import requests
import zipfile
import tempfile
from pathlib import Path
from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup

from pylipd.lipd import LiPD


def find_download_link(base_url="https://lipdverse.org/lipdverse/current_version/projectSidebar.html"):
    """
    Find the download link for "Download all LiPD files" from the LiPDverse page.
    
    Parameters
    ----------
    base_url : str
        The base URL of the LiPDverse current version page
        
    Returns
    -------
    str
        The full download URL for the LiPD files
    """
    print(f"Fetching download link from: {base_url}")
    
    try:
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for links containing "Download all LiPD files" or similar text
        download_link = None
        for link in soup.find_all('a', href=True):
            link_text = link.get_text(strip=True).lower()
            if 'download all lipd files' in link_text or 'download all' in link_text:
                href = link['href']
                # Make sure it's a full URL
                if href.startswith('http'):
                    download_link = href
                else:
                    download_link = urljoin(base_url, href)
                break
        
        if not download_link:
            # Fallback: look for .zip files
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.endswith('.zip') and ('lipd' in href.lower() or 'all' in href.lower()):
                    if href.startswith('http'):
                        download_link = href
                    else:
                        download_link = urljoin(base_url, href)
                    break
        
        if download_link:
            print(f"Found download link: {download_link}")
            return download_link
        else:
            raise ValueError("Could not find download link for LiPD files on the page")
            
    except Exception as e:
        print(f"Error fetching download link: {e}")
        raise


def download_file(url, local_filename):
    """
    Download a file from URL to local filename with progress indication.
    
    Parameters
    ----------
    url : str
        The URL to download from
    local_filename : str
        The local file path to save to
    """
    print(f"Downloading: {url}")
    print(f"Saving to: {local_filename}")
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        
        with open(local_filename, 'wb') as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}% ({downloaded:,} / {total_size:,} bytes)", end='')
    
    print(f"\nDownload completed: {local_filename}")


def extract_zip(zip_path, extract_to):
    """
    Extract a ZIP file to the specified directory.
    
    Parameters
    ----------
    zip_path : str
        Path to the ZIP file
    extract_to : str
        Directory to extract files to
    """
    print(f"Extracting {zip_path} to {extract_to}")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    print(f"Extraction completed")


def find_lipd_directory(base_dir):
    """
    Find the directory containing .lpd files after extraction.
    
    Parameters
    ----------
    base_dir : str
        The base directory to search in
        
    Returns
    -------
    str
        Path to the directory containing .lpd files
    """
    base_path = Path(base_dir)
    
    # Look for .lpd files recursively
    lipd_files = list(base_path.rglob("*.lpd"))
    
    if not lipd_files:
        raise ValueError(f"No .lpd files found in {base_dir}")
    
    # Find the common directory containing most .lpd files
    directories = [f.parent for f in lipd_files]
    most_common_dir = max(set(directories), key=directories.count)
    
    print(f"Found {len(lipd_files)} LiPD files")
    print(f"LiPD directory: {most_common_dir}")
    
    return str(most_common_dir)


def find_existing_lipd_files(search_dirs=None):
    """
    Find existing LiPD files in common locations.
    
    Parameters
    ----------
    search_dirs : list of str, optional
        Additional directories to search for existing LiPD files
        
    Returns
    -------
    list of Path
        List of existing .lpd file paths
    """
    existing_files = []
    
    # Default search locations
    default_dirs = []
    
    if search_dirs:
        default_dirs.extend(search_dirs)
    
    print("Searching for existing LiPD files...")
    
    for search_dir in default_dirs:
        search_path = Path(search_dir)
        if search_path.exists():
            lipd_files = list(search_path.rglob("*.lpd"))
            if lipd_files:
                print(f"Found {len(lipd_files)} existing LiPD files in: {search_path}")
                existing_files.extend(lipd_files)
    
    # Remove duplicates based on filename (keep first occurrence)
    unique_files = {}
    for file_path in existing_files:
        filename = file_path.name
        if filename not in unique_files:
            unique_files[filename] = file_path
    
    result = list(unique_files.values())
    if result:
        print(f"Total unique existing LiPD files found: {len(result)}")
    else:
        print("No existing LiPD files found")
    
    return result


def merge_lipd_files(downloaded_dir, existing_files, merged_dir):
    """
    Merge downloaded LiPD files with existing ones, avoiding duplicates.
    
    Parameters
    ----------
    downloaded_dir : str
        Directory containing newly downloaded LiPD files
    existing_files : list of Path
        List of existing LiPD file paths
    merged_dir : str
        Directory to store the merged collection
        
    Returns
    -------
    str
        Path to the merged directory
    """
    import shutil
    
    merged_path = Path(merged_dir)
    merged_path.mkdir(parents=True, exist_ok=True)
    
    # Copy downloaded files first
    downloaded_files = list(Path(downloaded_dir).glob("*.lpd"))
    downloaded_names = set()
    
    print(f"Copying {len(downloaded_files)} downloaded LiPD files...")
    for file_path in downloaded_files:
        dest_path = merged_path / file_path.name
        shutil.copy2(file_path, dest_path)
        downloaded_names.add(file_path.name)
    
    # Copy existing files that aren't already in downloaded collection
    existing_copied = 0
    for file_path in existing_files:
        if file_path.name not in downloaded_names:
            dest_path = merged_path / file_path.name
            if not dest_path.exists():  # Extra safety check
                shutil.copy2(file_path, dest_path)
                existing_copied += 1
                print(f"Added existing file: {file_path.name}")
    
    total_files = len(list(merged_path.glob("*.lpd")))
    
    print(f"Merge completed:")
    print(f"  - Downloaded files: {len(downloaded_files)}")
    print(f"  - Additional existing files: {existing_copied}")
    print(f"  - Total merged files: {total_files}")
    
    return str(merged_path)


def convert_to_rdf(lipd_dir, output_nq_file):
    """
    Convert LiPD files to RDF using PyLiPD.
    
    Parameters
    ----------
    lipd_dir : str
        Directory containing .lpd files
    output_nq_file : str
        Output .nq file path
    """
    print(f"Converting LiPD files from {lipd_dir} to RDF...")
    print(f"Output file: {output_nq_file}")
    
    # Initialize LiPD
    L = LiPD()
    
    # Convert LiPD files to RDF
    L.convert_lipd_dir_to_rdf(
        lipd_dir,
        output_nq_file,
        parallel=True,
        standardize=True,
        add_labels=False
    )
    
    print(f"RDF conversion completed: {output_nq_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Download and convert LiPDverse files to RDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--output-dir', 
        default='./lipdverse_data',
        help='Directory to store downloaded and processed files (default: ./lipdverse_data)'
    )
    
    parser.add_argument(
        '--nq-filename',
        default='all-lipd.nq',
        help='Name of the output .nq file (default: all-lipd.nq)'
    )
    
    parser.add_argument(
        '--keep-downloaded',
        action='store_true',
        help='Keep the downloaded ZIP and extracted LiPD files after conversion'
    )
    
    parser.add_argument(
        '--download-url',
        help='Override the download URL (useful if auto-detection fails)'
    )
    
    parser.add_argument(
        '--search-dirs',
        nargs='*',
        help='Additional directories to search for existing LiPD files'
    )
    
    parser.add_argument(
        '--skip-existing',
        action='store_true',
        help='Skip searching for existing LiPD files, only use downloaded ones'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    temp_dir = None
    try:
        # Create temporary directory for downloads
        temp_dir = tempfile.mkdtemp(prefix='lipdverse_')
        print(f"Using temporary directory: {temp_dir}")
        
        # Step 1: Find download link
        if args.download_url:
            download_url = args.download_url
            print(f"Using provided download URL: {download_url}")
        else:
            download_url = find_download_link()
        
        # Step 2: Download the ZIP file
        zip_filename = os.path.join(temp_dir, 'lipdverse_files.zip')
        download_file(download_url, zip_filename)
        
        # Step 3: Extract the ZIP file
        extract_dir = os.path.join(temp_dir, 'extracted')
        os.makedirs(extract_dir, exist_ok=True)
        extract_zip(zip_filename, extract_dir)
        
        # Step 4: Find the LiPD directory
        lipd_dir = find_lipd_directory(extract_dir)
        
        # Step 5: Find existing LiPD files
        if not args.skip_existing:
            existing_files = find_existing_lipd_files(args.search_dirs)
        else:
            existing_files = []
        
        # Step 6: Merge downloaded and existing LiPD files
        if existing_files:
            merged_dir = merge_lipd_files(lipd_dir, existing_files, os.path.join(temp_dir, 'merged'))
        else:
            print("No existing LiPD files to merge, using downloaded files only")
            merged_dir = lipd_dir
        
        # Step 7: Convert to RDF
        output_nq_path = output_dir / args.nq_filename
        convert_to_rdf(merged_dir, str(output_nq_path))
        
        # Step 8: Optionally copy files to output directory
        if args.keep_downloaded:
            import shutil
            saved_zip_path = output_dir / 'lipdverse_files.zip'
            saved_lipd_dir = output_dir / 'lipd_files'
            
            shutil.copy2(zip_filename, saved_zip_path)
            shutil.copytree(merged_dir, saved_lipd_dir, dirs_exist_ok=True)
            
            print(f"Downloaded files saved to:")
            print(f"  ZIP file: {saved_zip_path}")
            print(f"  LiPD files: {saved_lipd_dir}")
        
        print(f"\n✅ Success! All LiPD files converted to: {output_nq_path}")
        
        # Show file size
        if output_nq_path.exists():
            file_size = output_nq_path.stat().st_size
            print(f"Output file size: {file_size:,} bytes ({file_size / (1024*1024):.1f} MB)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
        
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
            print(f"Cleaned up temporary directory: {temp_dir}")


if __name__ == "__main__":
    main() 