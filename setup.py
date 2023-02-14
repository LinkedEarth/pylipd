import os

from setuptools import setup, find_packages


version = '0.9.8'

# Read the readme file contents into variable
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pylipd',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    version=version,
    license='Apache 2-0 License',
    description='Python utilities for handling LiPD data',
    long_description=read("README.md"),
    long_description_content_type = 'text/markdown',
    author='Varun Ratnakar',
    author_email='varunratnakar@gmail.com',
    url='https://github.com/linkedearth/pylipd',
    download_url='https://github.com/linkedearth/pylipd/tarball/'+version,
    keywords=['Paleoclimate, Data Analysis, LiPD'],
    package_dir = {'':'.'},
    classifiers=[],
    install_requires=[
        "rdflib",
        "pandas"
    ],
    python_requires=">=3.9.0"
)
