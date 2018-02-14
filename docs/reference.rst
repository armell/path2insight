=============
API Reference
=============

FilePath Objects
================

.. autoclass:: path2insight.WindowsFilePath
  :members:
  :inherited-members:

.. autoclass:: path2insight.PosixFilePath
  :members:
  :inherited-members:


Parsing
=======

.. autofunction:: path2insight.parse
.. autofunction:: path2insight.parse_from_list
.. autofunction:: path2insight.parse_from_numpy
.. autofunction:: path2insight.parse_from_pandas

Handling
========

.. autofunction:: path2insight.sort
.. autofunction:: path2insight.sample
.. autofunction:: path2insight.select
.. autofunction:: path2insight.select_re


Explore
=======

.. automodule:: path2insight.explore.stats
  :members:

.. automodule:: path2insight.explore.metrics
  :members:

Tokenizing
==========

.. automodule:: path2insight.tokenizers.tokenizers
  :members:

Tagging
=======

.. automodule:: path2insight.explore.tagger
  :members:
  :inherited-members:


Datasets
========

Create
------

.. autofunction:: path2insight.collect.walk


Examples
--------
Path2Insight comes with several datasets. These datasets are public and
real datasets. The datasets are available through the submodule 'datasets'.
See the example below:

.. code:: python
  
    from path2insight.datasets import load_pride

.. automodule:: path2insight.datasets.external
  :members:


Misc
====

.. automodule:: path2insight.external.nltk
  :members:
