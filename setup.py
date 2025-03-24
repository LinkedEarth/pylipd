import os
from setuptools import setup, find_packages

version = '1.4.0'

# Read the readme file contents into variable
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pylipd',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['data/*.lpd', 'data/Pages2k/*.lpd', 'globals/synonyms.json']},
    zip_safe=False,
    version=version,
    license='Apache-2.0',
    license_files=['LICENSE'],
    description='Python utilities for handling LiPD data',
    long_description=read("README.md"),
    long_description_content_type = 'text/markdown',
    author='Varun Ratnakar, Deborah Khider',
    author_email='varunratnakar@gmail.com',
    url='https://github.com/linkedearth/pylipd',
    download_url='https://github.com/linkedearth/pylipd/tarball/'+version,
    keywords=['Paleoclimate, Data Analysis, LiPD'],
    package_dir = {'':'.'},
    classifiers=[],
    install_requires=[
        "rdflib",
        "pandas",
        "doi2bib",
        "pybtex",
        "tqdm",
        "bagit",
        "numpy",
        "bibtexparser"
    ],
    python_requires=">=3.11.0"
)
