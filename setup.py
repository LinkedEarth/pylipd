import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pylipd",
    version="0.9.0",
    description="Python utilities for handling LiPD data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/linkedearth/pylipd",
    author="Varun Ratnakar",
    author_email="varunr@isi.edu",
    license="Apache-2",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
    ],
    packages=["pylipd"],
    include_package_data=True,
    install_requires=["rdflib", "chardet", "idna", "requests", "urllib3"],
)
