.. _installation:

Getting Started
===============

.. note::

   PyLiPD requires the use of Python 3.11 or above

Installation
""""""""""""

PyLiPD can be easily installed through `PyPI <https://pypi.org/project/pylipd/>`_. We recommend using an dedicated `Anaconda <https://docs.continuum.io/free/anaconda/>`_ or `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ environment. Then you may install PyLiPD via pip. Installation instructions for Anaconda can be found `here <https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html>`_.

Creating an environment  
++++++++++++++++++++++++

Create an environment via the command line:

.. code-block:: bash

  conda create -n lipd

As of September 2025, we recommend the use of Python 3.11. To install this specific version of Python, use the following:

.. code-block:: bash

  conda create -n lipd python=3.11

To view a list of available environments:

.. code-block:: bash

   conda env list

To activate the new environment:

.. code-block:: bash

   conda activate lipd

To view the list of packages in your environment:

.. code-block:: bash

   conda list

To remove the environment:

.. code-block:: bash

   conda remove --name lipd --all

More information about managing conda environments can be found `here <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#>`_.

Installing PyLiPD  
+++++++++++++++++

Once the lipd environment is activated, simply run:

.. code-block:: bash

  pip install pylipd

This will install the latest official release, which you can view `here <https://pypi.org/project/pylipd/>`_. To install the latest version, which contains the most up-to-date features, you can install directly from the GitHub source:

.. code-block:: bash

  pip install git+https://github.com/LinkedEarth/pylipd.git

This version may contain bugs not caught by our continuous integration test suite; if so, please report them via `github issues <https://github.com/LinkedEarth/pylipd/issues>`_. 

If you wish to contribute to PyLiPD, :ref:`see our contributing guide <contributing_to_pylipd>` for complete instructions on building from the git source tree. 

Running the test suite
""""""""""""""""""""""

pylipd comes with a set if unit tests. To run these, you need to install pytest in the same environment as pylipd via `pip install pytest`. To run the tests from a Python terminal, navigate to the tests folder on your computer and run:

.. code-block:: bash

   pytest

.. note::

   Since some of the tests require the use of the Graph Database, you need to have an internet connection for these tests to run.

Dependencies
""""""""""""

pylipd requires the following dependencies:

- rdflib
- Pandas
- doi2bib
- pybtex
- tqdm
- bagit
- numpy
- bibtexparser
- beautifulsoup4
- requests

Usage
"""""

Loading a local LiPD file
+++++++++++++++++++++++++

.. code-block:: bash

   from pylipd.lipd import LiPD
    lipd = LiPD()
    lipd.load(["MD98_2181.Stott.2007.lpd", "Ant-WAIS-Divide.Severinghaus.2012.lpd", "Asi-TDAXJP.PAGES2k.2013.lpd"])

Loading LiPD data from GraphDB server
+++++++++++++++++++++++++++++++++++++

.. code-block:: bash

   from pylipd.lipd import LiPD
    lipd = LiPD()
    lipd.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse-dynamic")
    lipd.load_remote_datasets(["MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012", "Asi-TDAXJP.PAGES2k.2013"])

