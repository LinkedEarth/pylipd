.. PyLiPD documentation master file, created by
   sphinx-quickstart on Fri Feb 10 15:48:28 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

PyLiPD is a Python package for handling (`LiPD <http://lipd.net>`_) datasets. 

.. image:: PyLiPD-Arch.png
   :width: 720px
   :height: 405px
   :scale: 100 %
   :alt: The PyLiPD Architecture. Credit: Varun Ratnakar

PyLiPD loads the Linked Paleo Data (`LiPD <http://lipd.net>`_), either locally or online, and converts them internally into (`RDF graphs <https://en.wikipedia.org/wiki/Resource_Description_Framework#:~:text=RDF%20is%20a%20directed%20graph,be%20identified%20by%20a%20URI.>`_) for further querying. Alternatively, PyLiPD can also read an RDF Knowledge Base like GraphDB directly that is populated by the LiPD datasets converted into RDF graphs. In short, it allows you to work seamlessly with LiPD files stored on your computer, on the web or in a dedicated database meant to work with graphs.

PyLiPD can use the internal/remote graph representation to either answer (`SparQL <https://www.ontotext.com/knowledgehub/fundamentals/what-is-sparql/>`_)  queries about the datasets, or simply convert it back to LiPD, or get the TimeSeries objects across multiple datasets for further analysis by packages such as (`Pyleoclim <https://pyleoclim-util.readthedocs.io/en/latest/>`_).

The package makes working with the Graph representation easier. You do no need to learn SparQL to start working with PyLiPD. However, SparQL is a fast, efficient language that makes querying much easier so we won't stop you from learning it. 

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
