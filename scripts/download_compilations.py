#!/usr/bin/env python3
"""
LiPD Compilation Downloader

This script downloads LiPD files for all compilations from LiPDverse.

Usage:
    python download_compilations.py [--output-dir OUTPUT_DIR] [--compilations COMP1,COMP2,...]
"""

import os
import sys
import argparse
import requests
import zipfile
import tempfile
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm


class LiPDCompilationDownloader:
    def __init__(self, output_dir="lipd_compilations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Download statistics
        self.download_stats = {
            'total_compilations_attempted': 0,
            'successful_downloads': 0,
            'failed_downloads': 0,
            'total_files_downloaded': 0,
            'download_details': []
        }

    def get_available_compilations(self):
        """Get list of available compilations by parsing the LiPDverse project page"""
        project_page_url = "https://lipdverse.org/project/"
        
        print("Fetching available compilations from LiPDverse...")
        
        try:
            response = requests.get(project_page_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find compilation links following the pattern:
            # <h2><a href="https://lipdverse.org/project/rapidarcticwarming/">RapidArcticWarming</a></h2>
            compilations = {}
            
            for h2_tag in soup.find_all('h2'):
                link_tag = h2_tag.find('a', href=True)
                if link_tag and link_tag['href'].startswith('https://lipdverse.org/project/'):
                    compilation_name = link_tag.get_text(strip=True)
                    project_url = link_tag['href']
                    
                    # Skip generic links that aren't compilations
                    if compilation_name and compilation_name not in ['Projects', 'Home', 'Articles']:
                        compilations[compilation_name] = project_url
            
            print(f"Found {len(compilations)} available compilations:")
            for name in sorted(compilations.keys()):
                print(f"  - {name}")
            
            return compilations
            
        except Exception as e:
            print(f"Error fetching compilations from project page: {e}")
            print("Falling back to known compilations...")
            
            # Fallback to known compilations if the web request fails
            known_compilations = {
                "CoralHydro2k": "https://lipdverse.org/project/coralhydro2k/",
                "HoloCoral": "https://lipdverse.org/project/holocoral/", 
                "HoloceneAbruptChange": "https://lipdverse.org/project/holoceneabruptchange/",
                "HoloceneHydroclimate": "https://lipdverse.org/project/holocenehydroclimate/",
                "Hydro21k": "https://lipdverse.org/project/hydro21k/",
                "LakeStatus21k": "https://lipdverse.org/project/lakestatus21k/",
                "Pages2kTemperature": "https://lipdverse.org/project/pages2ktemperature/",
                "RapidArcticWarming": "https://lipdverse.org/project/rapidarcticwarming/",
                "SISAL-LiPD": "https://lipdverse.org/project/sisal/",
                "Temp12k": "https://lipdverse.org/project/temperature12k/",
                "Temp24k": "https://lipdverse.org/project/temp24k/",
                "iso2k": "https://lipdverse.org/project/iso2k/",
                "wNAm": "https://lipdverse.org/project/wnam/"
            }
            return known_compilations

    def find_download_link(self, compilation_name, project_url):
        """
        Find the download link for a specific compilation using its project page URL.
        """
        print(f"Looking for download link: {compilation_name}")
        print(f"  Project page: {project_url}")
        
        try:
            # First, get the project page to find the data link
            response = requests.get(project_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the data link following the pattern:
            # <h2><a href="http://lipdverse.org/RapidArcticWarming/current_version/">Data</a></h2>
            data_url = None
            
            for h2_tag in soup.find_all('h2'):
                link_tag = h2_tag.find('a', href=True)
                if link_tag and link_tag.get_text(strip=True).lower() == 'data':
                    data_url = link_tag['href']
                    break
            
            # Alternative search - look for links containing "current_version"
            if not data_url:
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    link_text = link.get_text(strip=True).lower()
                    if 'current_version' in href and ('data' in link_text or 'access' in link_text):
                        data_url = href
                        break
            
            if not data_url:
                print(f"  No data link found on project page for {compilation_name}")
                return None
            
            print(f"  Found data page: {data_url}")
            
            # Now search for download links on the data page
            base_url = data_url
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
            
            # Try main data page first
            try:
                response = requests.get(main_url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                download_url = search_for_download_links(main_url, soup)
                
                if download_url:
                    print(f"  Found download link: {download_url}")
                    return download_url
                    
            except Exception as e:
                print(f"  Error accessing data page for {compilation_name}: {e}")
            
            # Try sidebar page
            try:
                response = requests.get(sidebar_url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                download_url = search_for_download_links(sidebar_url, soup)
                
                if download_url:
                    print(f"  Found download link on sidebar: {download_url}")
                    return download_url
                    
            except Exception as e:
                print(f"  Error accessing sidebar for {compilation_name}: {e}")
            
        except Exception as e:
            print(f"  Error accessing project page for {compilation_name}: {e}")
        
        print(f"  No download link found for {compilation_name}")
        return None

    def cleanup_macos_artifacts(self, directory):
        """Remove macOS artifacts like __MACOSX directories and .DS_Store files."""
        directory = Path(directory)
        cleanup_count = 0
        
        # Find and remove __MACOSX directories
        macosx_dirs = list(directory.rglob("__MACOSX"))
        for macosx_dir in macosx_dirs:
            if macosx_dir.is_dir():
                try:
                    import shutil
                    shutil.rmtree(macosx_dir)
                    cleanup_count += 1
                    print(f"    Removed: {macosx_dir}")
                except Exception as e:
                    print(f"    Warning: Could not remove {macosx_dir}: {e}")
        
        # Find and remove .DS_Store files
        dsstore_files = list(directory.rglob(".DS_Store"))
        for dsstore_file in dsstore_files:
            try:
                dsstore_file.unlink()
                cleanup_count += 1
                print(f"    Removed: {dsstore_file}")
            except Exception as e:
                print(f"    Warning: Could not remove {dsstore_file}: {e}")
        
        # Find and remove resource fork files (._filename)
        resource_fork_files = list(directory.rglob("._*"))
        for rf_file in resource_fork_files:
            if rf_file.is_file():
                try:
                    rf_file.unlink()
                    cleanup_count += 1
                    print(f"    Removed: {rf_file}")
                except Exception as e:
                    print(f"    Warning: Could not remove {rf_file}: {e}")
        
        if cleanup_count > 0:
            print(f"    ✓ Cleaned up {cleanup_count} macOS artifacts")

    def download_compilation(self, compilation_name, download_url):
        """
        Download and extract LiPD files for a compilation.
        """
        compilation_dir = self.output_dir / f"{compilation_name}"
        compilation_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Downloading {compilation_name} from {download_url}")
        
        try:
            # Download the file
            response = requests.get(download_url, timeout=300)
            response.raise_for_status()
            
            # Parse filename from URL or Content-Disposition header
            filename = None
            if 'Content-Disposition' in response.headers:
                content_disp = response.headers['Content-Disposition']
                if 'filename=' in content_disp:
                    filename = content_disp.split('filename=')[1].strip('"\'')
            
            if not filename:
                parsed_url = urlparse(download_url)
                filename = os.path.basename(parsed_url.path)
                if not filename or not filename.endswith('.zip'):
                    filename = f"{compilation_name}.zip"
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
                temp_file.write(response.content)
                temp_zip_path = temp_file.name
            
            print(f"  Downloaded {len(response.content)} bytes")
            
            # Extract ZIP file
            extracted_count = 0
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.endswith('.lpd'):
                        # Extract to compilation directory
                        zip_ref.extract(file_info, compilation_dir)
                        extracted_count += 1
            
            print(f"  Extracted {extracted_count} LiPD files to {compilation_dir}")
            
            # Clean up macOS artifacts after extraction
            self.cleanup_macos_artifacts(compilation_dir)
            
            # Clean up temporary file
            os.unlink(temp_zip_path)
            
            # Update stats
            self.download_stats['total_files_downloaded'] += extracted_count
            self.download_stats['download_details'].append({
                'compilation': compilation_name,
                'files_count': extracted_count,
                'directory': str(compilation_dir),
                'status': 'success'
            })
            
            return compilation_dir if extracted_count > 0 else None
            
        except Exception as e:
            print(f"  Error downloading {compilation_name}: {e}")
            self.download_stats['download_details'].append({
                'compilation': compilation_name,
                'files_count': 0,
                'directory': None,
                'status': 'failed',
                'error': str(e)
            })
            return None

    def download_all_compilations(self, specific_compilations=None):
        """
        Download all available compilations or specific ones.
        """
        print("Starting LiPD Compilation Download Process")
        print("=" * 50)
        
        available_compilations = self.get_available_compilations()
        
        if specific_compilations:
            # Validate requested compilations - filter the dict by requested compilation names
            invalid_compilations = set(specific_compilations) - set(available_compilations.keys())
            if invalid_compilations:
                print(f"Warning: Unknown compilations requested: {invalid_compilations}")
            
            # Create a filtered dict of compilations to download
            compilations_to_download = {
                name: url for name, url in available_compilations.items() 
                if name in specific_compilations
            }
        else:
            compilations_to_download = available_compilations
        
        print(f"Will attempt to download {len(compilations_to_download)} compilations:")
        for comp in sorted(compilations_to_download.keys()):
            print(f"  - {comp}")
        print()
        
        self.download_stats['total_compilations_attempted'] = len(compilations_to_download)
        
        # Download each compilation
        for compilation_name, project_url in tqdm(sorted(compilations_to_download.items()), desc="Downloading compilations"):
            try:
                download_url = self.find_download_link(compilation_name, project_url)
                
                if download_url:
                    result = self.download_compilation(compilation_name, download_url)
                    if result:
                        self.download_stats['successful_downloads'] += 1
                        print(f"  ✓ Successfully downloaded {compilation_name}")
                    else:
                        self.download_stats['failed_downloads'] += 1
                        print(f"  ✗ Failed to download {compilation_name}")
                else:
                    self.download_stats['failed_downloads'] += 1
                    print(f"  ✗ No download link found for {compilation_name}")
                    
            except Exception as e:
                self.download_stats['failed_downloads'] += 1
                print(f"  ✗ Error processing {compilation_name}: {e}")
        
        self.generate_download_report()

    def generate_download_report(self):
        """Generate a summary report of the download process."""
        report_path = self.output_dir / "download_report.txt"
        
        print("\n" + "=" * 50)
        print("Download Process Complete!")
        print(f"Total compilations attempted: {self.download_stats['total_compilations_attempted']}")
        print(f"Successful downloads: {self.download_stats['successful_downloads']}")
        print(f"Failed downloads: {self.download_stats['failed_downloads']}")
        print(f"Total LiPD files downloaded: {self.download_stats['total_files_downloaded']}")
        print(f"Files saved to: {self.output_dir}")
        
        with open(report_path, 'w') as f:
            f.write("LiPD Compilation Download Report\n")
            f.write("=" * 35 + "\n\n")
            
            f.write(f"Total compilations attempted: {self.download_stats['total_compilations_attempted']}\n")
            f.write(f"Successful downloads: {self.download_stats['successful_downloads']}\n")
            f.write(f"Failed downloads: {self.download_stats['failed_downloads']}\n")
            f.write(f"Total LiPD files downloaded: {self.download_stats['total_files_downloaded']}\n\n")
            
            f.write("Detailed Results:\n")
            f.write("-" * 20 + "\n")
            
            for detail in self.download_stats['download_details']:
                f.write(f"\nCompilation: {detail['compilation']}\n")
                f.write(f"Status: {detail['status']}\n")
                f.write(f"Files downloaded: {detail['files_count']}\n")
                if detail['directory']:
                    f.write(f"Directory: {detail['directory']}\n")
                if 'error' in detail:
                    f.write(f"Error: {detail['error']}\n")
        
        print(f"Report generated: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Download LiPD compilation files from LiPDverse",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all available compilations
  python download_compilations.py

  # Download specific compilations
  python download_compilations.py --compilations Temp12k,Pages2kTemperature

  # Specify custom output directory
  python download_compilations.py --output-dir /path/to/output
        """
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='lipd_compilations',
        help='Output directory for downloaded files (default: lipd_compilations)'
    )
    
    parser.add_argument(
        '--compilations',
        type=str,
        help='Comma-separated list of specific compilations to download (default: all available)'
    )
    
    args = parser.parse_args()
    
    # Parse compilations list
    specific_compilations = None
    if args.compilations:
        specific_compilations = [comp.strip() for comp in args.compilations.split(',')]
    
    # Create and run the downloader
    downloader = LiPDCompilationDownloader(output_dir=args.output_dir)
    
    try:
        downloader.download_all_compilations(specific_compilations)
    except KeyboardInterrupt:
        print("\nDownload process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
