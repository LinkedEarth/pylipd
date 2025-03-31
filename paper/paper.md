---
title: 'PyLiPD: A python package for the manipulation of paleoclimate datasets'
tags:
  - Python
  - paleoclimate
  - knowledge graph
authors:
  - name: Varun Ratnakar
    orcid: 0000-0001-9381-705X
    affiliation: 1
  - name: Deborah Khider
    orcid: 0000-0001-7501-8430
    affiliation: 1
affiliations:
 - name: Information Sciences Institute, University of Southern California
   index: 1
date: 24 March 2025
bibliography: paper.bib
---

# PyLiPD: a Python package for manipulating LiPD datasets

## Summary
PyLiPD is an open-source Python library for accessing and manipulating paleoclimate datasets stored in the Linked PaleoData (LiPD) format. LiPD is a standardized data format, based on JSON-LD, designed to organize paleoclimate data and metadata in a uniform, machine-readable way. PyLiPD allows researchers to load LiPD files, query their contents, and seamlessly integrate these datasets into Python-based analysis workflows. It also interfaces directly with remote LiPD databases via SPARQL endpoints, bridging standardized paleoclimate data to the broader scientific Python ecosystem, such as analysis tools like Pyleoclim [@Khider2022].

## Background
Paleoclimate data (proxy measurements from ice cores, sediments, corals, etc.) often come with diverse structures and metadata conventions, making synthesis efforts challenging. Community-driven initiatives like PAGES 2k have compiled paleoclimate records into unified data collections, highlighting the necessity of standardized data formats. The Linked PaleoData (LiPD) framework emerged to address this need, providing a common JSON-LD-based format for paleoclimate information [@McKay2016]. LiPD standardization facilitates efficient querying and analysis of multiple records, enabling large-scale climate reconstructions [@Kaufman2020]. PyLiPD was developed as part of the broader LiPD ecosystem to empower paleoclimate researchers using Python.

## Statement of Need
Prior to PyLiPD, there was no dedicated Python library for LiPD datasets, posing challenges for Python-based workflows. Researchers had to either rely on tools from other languages or manually handle complex JSON-LD data structures. PyLiPD fills this gap by providing simple Python interfaces for reading, querying, and writing LiPD data. It abstracts complexities of LiPD's underlying structure and linked-data queries, significantly lowering barriers to using large paleoclimate compilations in Python. This capability is particularly important for enabling reproducible and efficient research workflows and integrating paleoclimate datasets with popular Python analysis libraries [@Khider2022].

## Technical Details
PyLiPD is implemented in Python (compatible with Python 3.x) and is distributed via PyPI. The library employs an object-oriented design centered around the `LiPD` class, which encapsulates LiPD datasets as RDF graphs using the LinkedEarth ontology [@LinkedEarthOntology]. PyLiPD provides functionality to load local or remote LiPD datasets, execute simple or complex SPARQL queries, and convert paleoclimate records into Python data structures like pandas DataFrames for further analysis. 

An important feature of PyLiPD is its integration with the GraphDB LiPDVerse, a graph database repository hosted at [https://linkedearth.graphdb.mint.isi.edu/](https://linkedearth.graphdb.mint.isi.edu/). This integration enables users to store, retrieve, and efficiently query LiPD data directly from this centralized graph repository, further promoting interoperability and extensibility within the paleoclimate research community.

PyLiPD is released under the Apache 2.0 license and is actively maintained as part of the LinkedEarth project, aiming to promote best practices in paleoclimate data handling.