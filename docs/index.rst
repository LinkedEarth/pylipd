.. PyLiPD documentation master file, created by
   sphinx-quickstart on Fri Feb 10 15:48:28 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

PyLiPD is a Python package for handling LiPD datasets. 

.. image:: PyLiPD-Arch.png
   :width: 720px
   :height: 405px
   :scale: 100 %
   :alt: The PyLiPD Architecture. Credit: Varun Ratnakar

PyLiPD loads the Linked Paleo Data (`LiPD <http://lipd.net>`_), either locally or online, and converts them internally into RDF graphs for further querying. Alternatively, PyLiPD can also read an RDF Knowledge Base like GraphDB directly that is populated by the LiPD datasets converted into RDF graphs. 

PyLiPD can use the internal/remote graph representation to either answer SparQL queries about the datasets, or simply convert it back to LiPD, or get the TimeSeries objects across multiple datasets for further analysis by packages such as Pyleoclim

Getting Started
===============

.. toctree::
   :maxdepth: 1
   :caption: Working with PyLiPD

   installation.rst
   api.rst
   tutorials.rst
   
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
