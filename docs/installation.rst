=============================
Installation and dependencies
=============================

Path2Insight is available on Pypi. This make it possible to install it with
through:

.. code:: bash

    pip install path2insight

To upgrade path2insight use 

.. code:: bash

    pip install --upgrade path2insight

It is also possible to install from source:

.. code:: bash

    python setup.py install 

Path2Insight is available for Python 2.7 and Python 3.4+. Path2Insight depends
heavily on the pathlib_ module. This module is part of Python 3.4 or higher.
For Python 2, the backport pathlib2_ is used. Therefore, it is advised to use
Path2Insight with Python 3.4 or higher.

.. _pathlib: https://docs.python.org/3/library/pathlib.html
.. _pathlib2: https://pypi.python.org/pypi/pathlib2/

Some of the submodules of Path2Insight depend on other Python packages (numpy,
pandas, sklearn, scipy, jellyfish). One can get a full installation by
installing the packages in the `requirements-full.txt` file.

.. code:: bash

    pip install -r requirements-full.txt

Docs 
----

The documentation for Path2Insight is available on readthedocs_. To generate
the docs by yourself, install the following packages (available on pip):

- sphinx
- sphinx_rtd_theme
- nbsphinx
  
.. code:: bash

    pip install -r docs/requirements-docs.txt

Navigate to the `docs/` folder and call `make html` or `make pdf` for a pdf
version.

.. _readthedocs: https://path2insight.readthedocs.com


Development and Testing 
-----------------------

Clone/fork the latest version of the Path2Insight from Github. 

.. code:: bash

    git clone github.com/armell/path2insight

Install the module in the development mode. 

.. code:: bash

    python setup.py develop

Path2Insight makes use of PyTest_ for unit testing. Run the tests with the
command:

.. _PyTest: https://docs.pytest.org/

.. code:: bash

    pytest
