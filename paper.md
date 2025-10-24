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
date: 25 April 2025
bibliography: paper.bib
---

# Summary
`PyLiPD` is a Python package designed to support the reading, querying, editing, and writing of paleoclimate datasets formatted in the Linked Paleo Data Format (LiPD) [@McKay2016]. Built on the `rdflib` library, it transforms LiPD data into Resource Description Framework (RDF) graphs aligned with the LinkedEarth ontology, enabling semantic querying with the SPARQL Protocol and RDF Query  (SPARQL). The API is structured into four modules that handle data access, variable-level filtering, and dataset creation and editing, with support for both graph-based and tabular workflows. Comprehensive documentation and tutorials—including ontology concepts and scientific use cases—are provided to guide users. 

# Statement of Need
Paleoclimate data (obtained from biogeophysical measurements made on ice cores, sediments, corals, trees, etc.) often come with diverse structures and metadata conventions, making synthesis efforts challenging and highlighting the necessity of standardized data formats.  Achieving standardization involves three key components: (1) a uniform data format, (2) a consistent terminology for describing metadata, and (3) clear guidelines for how data should be reported. The LiPD framework emerged to address the first need, providing a universally readable data container for paleoclimate data and metadata [@McKay2016]. The metadata is stored in a JSON-LD file while the data is organized in multiple tables saved as csv files. LiPD has six distinct components: root metadata (e.g., dataset name, and version); geographic metadata (e.g., coordinates); publication metadata (including unique identifiers); funding metadata (e.g., grant number); PaleoData, which includes all the measured (e.g., the width of tree rings) and inferred (e.g., temperature) paleoenvironmental data; and ChronData, which mirrors PaleoData for information pertaining to time. These components provide the rigidity necessary to write robust codes around the format while remaining extensible enough to capture (meta)data as rich as the users want to provide for them. Paired with the Paleoenvironmental Standard Terms (PaST) Thesaurus developed by the National Oceanic and Atmospheric Administration (NOAA) [@Morrill2021], LiPD standardization facilitates efficient querying and analysis of multiple records, enabling large-scale paleoclimate syntheses. Community-driven initiatives to reconstruct temperature and hydroclimate over Earth's history [@pages2k; @Kaufman2020; @Routson2021; @Konecky2020; @Jonkers2020] have compiled paleoclimate records into this standardized format and have made them available to the paleoclimate community in an [online database](https://lipdverse.org). As the database continued to grow, there was an increasing demand for tools capable of accessing, reading, modifying, and writing files in the LiPD format. Although there is a package in R [@LipdR], a Python tool built for scientists and interoperable with libraries such as `Pyleoclim` [@Khider2022] for time series analysis and `cfr` [@Zhu2024] for climate field reconstruction is lacking. To address this need, we introduce `PyLiPD`, a Python-based tool designed specifically for these tasks.

# Implementation
PyLiPD is built on top of the Python `rdflib` library [@Krech_RDFLib_2025], which supports working with RDF data and provides robust capabilities for parsing, manipulating, and querying semantic graphs using SPARQL. To leverage this functionality, LiPD-formatted datasets are converted into RDF graphs upon loading, using the LinkedEarth ontology [@LinkedEarthOntology]. The LinkedEarth Ontology captures the LiPD components and the relationship among them and integrates the standardized terms from the PaST Thesaurus.  

`PyLiPD`'s user-facing APIs are organized around four main modules. The `LiPD` module allows users to load, manipulate, query, and filter LiPD-formatted datasets stored locally, retrieved via URL, or accessed from an online knowledge base. The API supports typical paleoclimate research queries, including filters by geographic extent, archive type, and temporal coverage. For users more comfortable with tabular formats, graph content can be flattened into a `pandas.DataFrame`. This feature facilitates integration with familiar data analysis tools in the Python ecosystem. Because the LiPD object is a subclass of `rdflib.Graph`, it also supports direct SPARQL querying. Given that PyLiPD's querying capabilities are largely built on `rdflib`'s SPARQL integration, the `pylipd.globals.queries` module includes a range of examples to illustrate common use cases. The `LiPDSeries` module provides functionality for querying and filtering data at the variable level.


All other modules -- `pylipd.classes`  (referred to as LiPD Classes in the documentation) -- and their associated submodules are primarily used for editing and creating LiPD-formatted datasets. Some of the modules (e.g., `pylipd.classes.dataset`, `pylipd.classes.variable`) include Python classes auto-generated from ontology definitions, each equipped with methods to `get`, `set`, or append (`add`) property values. Others (e.g., `pylipd.classes.archivetype`, `pylipd.classes.paleovariable`) are used to align with the PaST Thesaurus, offering standardized vocabularies for properties such as variable names, archive types, and units. 

The APIs are fully documented and include minimal working examples. Documentation is available on [Read the Docs](https://pylipd.readthedocs.io/en/latest/index.html), where users can also find installation instructions and guidelines for contributing to the codebase.

# Research Applications

In addition to the minimal working examples in the documentation, more comprehensive tutorials [@PyLipdTutorials] are available as a [Jupyter Book](http://linked.earth/pylipdTutorials/intro.html). These tutorials introduce key ontology concepts—particularly the LinkedEarth Ontology—and offer scientific use cases that demonstrate how to apply the PyLiPD software.

# Availability

PyLiPD is an open-source software released under the Apache 2.0 license and is actively maintained as part of the LinkedEarth project. It is available through [PyPi](https://pypi.org/project/pylipd/) and [GitHub](https://github.com/linkedearth/pylipd). Documentation is available through [readthedocs](https://pylipd.readthedocs.io/en/latest/index.html).

# Acknowledgements

This work is supported by the US National Science Foundation grant RISE 2126510 to Khider. 

# References
