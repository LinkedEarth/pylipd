.. _tutorials:

Tutorials
=========

This page contains a few tutorials for using PyLiPD.  

.. grid:: 3
   :gutter: 2
   :margin: 2

   .. card::
      :img-top: _static/thumbs/01_intro.png
      :link: https://linked.earth/pylipdTutorials/intro.html
      :text-align: left

      **An Introduction to the PyLiPD Package**
      Provides an overview of the package and the tutorials


Dataset Representation in PyLiPD
""""""""""""""""""""""""""""""""

We recommend reading these tutorials if you want to get a deeper understanding of how the datasets are represented. These tutorials are mandatory reading for anyone creating custom queries or needing to create/edit a LiPD file.

.. grid:: 3
   :gutter: 2
   :margin: 2

   .. card::
      :img-top: _static/thumbs/02_DataRep.png
      :link: https://linked.earth/pylipdTutorials/graph.html
      :text-align: left

      **Understanding how datasets are represented in PyLiPD**
      This tutorial provides an overview of the ontology and the SPARQL language

   .. card::
      :img-top: _static/thumbs/03_Stds.png
      :link: https://linked.earth/pylipdTutorials/standards.html
      :text-align: left

      **Standard, Standards, and More Standards**
      This tutorial provides an overview of the vocabulary used for the values of certain terms such as archive and proxy.
      
Getting Started
"""""""""""""""
.. grid:: 3
   :gutter: 2
   :margin: 2

   .. card::
      :img-top: _static/thumbs/04_Loading.png
      :link: https://linked.earth/pylipdTutorials/notebooks/L0_a_loading_lipd_datasets.html
      :text-align: left

      **Reading LiPD formatted datasets with PyLiPD**
      This tutorial provides examples on how to load local files, files in a directory, from a URL, and from the GraphDB. 

   .. card::
      :img-top: _static/thumbs/05_Manip.png
      :link: https://linked.earth/pylipdTutorials/notebooks/L0_b_lipd_object.html
      :text-align: left

      **Basic Manipulation of pylipd.LiPD objects**
      This tutorial shows how to extract information (data and associated metadata) from LiPD files and how to add and remove datasets from an existing object.


Basic Functionalities
"""""""""""""""""""""
.. grid:: 3
   :gutter: 2
   :margin: 2

   .. card::
      :img-top: _static/thumbs/06_Ensembles.png
      :link: https://linked.earth/pylipdTutorials/notebooks/L1_a_working_with_ensembles.html
      :text-align: left

      **Working with ensembles in PyLiPD**
      This tutorial describes how PyLiPD deals with age ensembles often used for uncertainty quantification in paleoclimate studies. 

   .. card::
      :img-top: _static/thumbs/07_Text.png
      :link: https://linked.earth/pylipdTutorials/notebooks/L1_b_getting_information.html
      :text-align: left

      **Retrieving textual information from LiPD files**
      This tutorial demonstrates the use of pre-defined APIs to get specific information from a LiPD file. 
   
   .. card::
      :img-top: _static/thumbs/08_Filters.png
      :link: https://linked.earth/pylipdTutorials/notebooks/L1_c_filtering.html
      :text-align: left

      **Filtering through queries**
      This tutorial demonstrates the use of existing APIs to filter records by location, type of archive, type of variables.

Advanced Querying using SPARQL
""""""""""""""""""""""""""""""

Although PyLiPD comes with many querying APIs, we recognize that we cannot cover every use case. These tutorials teach you how to use the SPARQL language to query the datasets directly. One of the advantages of using a graph representation is that rich metadata information can be stored and accessed. That level of query specificity comes at a price: learning the SPARQL language. 

.. grid:: 3
   :gutter: 2
   :margin: 2

   .. card::
      :img-top: _static/thumbs/09_Queries.png
      :link: https://linked.earth/pylipdTutorials/notebooks/L2_a_custom_queries.html
      :text-align: left

      **Custom queries on LiPD objects**
      This tutorial provides examples of custom queries of LiPD object using the SPARQL language. 

   .. card::
      :img-top: _static/thumbs/10_GraphDB.png
      :link: https://linked.earth/pylipdTutorials/notebooks/L2_b_using_graphdb.html
      :text-align: left

      **Directly querying the LiPDGraph**
      This tutorial demonstrates the use of the SPAQRL endpoint on LiPDGraph to directly retrieve relevant information.
   

As you may have guessed, many of our existing PyLiPD functionalities are wrappers around custom SPARQL queries, which are stored in `this Python file <https://github.com/LinkedEarth/pylipd/blob/main/pylipd/globals/queries.py>`_. Feel free to use them as inspiration!

Editing LiPD files
""""""""""""""""""

.. grid:: 3
   :gutter: 2
   :margin: 2

   .. card::
      :img-top: _static/thumbs/11_Dataset.png
      :link: https://linked.earth/pylipdTutorials/notebooks/L3_a_dataset_class.html
      :text-align: left

      **The Dataset class**
      This tutorial describes how PyLiPD relates to the LinkedEarth ontology and how it can be leveraged to create/edit LiPD files. 
   
   .. card::
      :img-top: _static/thumbs/12_Editing.png
      :link: https://linked.earth/pylipdTutorials/notebooks/L3_b_editing.html
      :text-align: left

      **Editing LiPD Files**
      This tutorial walks through the process of editing an existing LiPD file. 
   
   .. card::
      :img-top: _static/thumbs/13_Creating.png
      :link: https://linked.earth/pylipdTutorials/notebooks/L1_c_filtering.html
      :text-align: left

      **Creating LiPD files from a tabular template**
      This tutorial shows an example on how to create a LiPD file from existing data in tabular format. 



