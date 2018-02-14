Path2Insight 
============

|travis| |readthedocs|

.. |travis| image:: https://travis-ci.org/armell/path2insight.svg?branch=master
    :target: https://travis-ci.org/armell/path2insight
.. |readthedocs| image:: https://readthedocs.org/projects/path2insight/badge/
    :target: https://readthedocs.org/projects/path2insight/badge/

Path2Insight (p2i) is a modular and scalable python module which aims at
offering a unified and comprehensive set of processing tools for analyzing
file paths. P2i supports static file systems analysis without requiring access
to the original physical storage. Basically, a scan of the storage’s content
exported as a text file suffices to explore the saved resources. There is also
no need to access the content of the files as the p2i module import file paths
as strings.

Once loaded, the file paths are stored in-memory as a python object enabling:
preprocessing, text processing and descriptive analysis of folders and files.

**Preprocessing:** Sample, sort and select files based on multiple criteria (e.g.
parent folder, depth).

**Text processing:** Chunk file paths into tokens (full path, stem and name),
n-grams or complete paths with the help of several extensible tokenizers.
Also, taggers offer the option to aggregate files based on their structure and
content (which prepare paths for further analysis such as entity recognition
or classification tasks).

**Descriptive analysis:** P2i implements counters for tokens, stems and
extensions. It supports also statistical features such as X2 tests on the
distribution of extensions, stems and names. Further, a representation of the
complexity of the folder structure is facilitated by folder-depth analysis
functionalities.

The table below shows how Path2Insight differ and complement functionalities
offered by lower-level python modules (pathlib and os.path).

+--------------------------------------------+-----------------------------------------------------------------------------------------+------------------------------------------+----------------------------------------------+
| Functionality                              | P2i                                                                                     | Pathlib                                  | os.path                                      |
+============================================+=========================================================================================+==========================================+==============================================+
| Preprocessing                              | Pathlib + Sampling, sorting, selection                                                  | match, joinpath                          | Normcase, norm path                          |
+--------------------------------------------+-----------------------------------------------------------------------------------------+------------------------------------------+----------------------------------------------+
| Descriptive statistics                     | Counters: stem, extension, name. Taggers. Tokenizers                                    | os.stat                                  | os.stat                                      |
+--------------------------------------------+-----------------------------------------------------------------------------------------+------------------------------------------+----------------------------------------------+
| Text processing                            | Pathlib + Tokens, n-grams, taggers, lower, upper,...                                    | Stem, name, parent, extension drive, ... | Split                                        |
+--------------------------------------------+-----------------------------------------------------------------------------------------+------------------------------------------+----------------------------------------------+
| Access or modify information on the system | No, can be linked to additional metadata (datetimes, users) by joining on the full path | Yes, chmod, current folder. ...          | Yes, user, size, datetimes, descriptors, ... |
+--------------------------------------------+-----------------------------------------------------------------------------------------+------------------------------------------+----------------------------------------------+

P2i is dependency free (only pathlib2 is required for Python 2.7 users), fast
and scalable path processing toolkit. It is compliant with the major data
analysis python modules such as pandas, scikit-learn, nltk and matplotlib to
extent the analytical possibilities of path2insight.

Example
=======

Import the module and load a demo dataset with static file paths (or use
`path2insight.walk` to collect from you file system).

.. code:: python

    >>> import path2insight
    >>> from path2insight.datasets import load_ensembl

    >>> filepaths = load_ensembl()

.. code:: python 

    >>> path2insight.depth_counts(filepaths)
    Counter({3: 1, 4: 11, 5: 39424, 6: 5543, 7: 2733, 8: 3388})

.. code:: python

    >>> path2insight.token_counts(filepaths).most_common(10)
    [('txt', 31977),
     ('gene', 13798),
     ('ensembl', 12727),
     ('dm', 12500),
     ('homolog', 7380),
     ('fa', 5890),
     ('chromosome', 5011),
     ('feature', 4878),
     ('dna', 4608),
     ('90', 3404)]

.. code:: python

    >>> path2insight.extension_counts(filepaths).most_common(10)
    [('.gz', 44427),
     ('', 3094),
     ('.bb', 847),
     ('.nsq', 349),
     ('.nin', 349),
     ('.nhr', 349),
     ('.tsv', 336),
     ('.psq', 250),
     ('.pin', 250),
     ('.phr', 250)]

.. code:: python

    >>> path2insight.select_re(filepaths, level5='micro.*')
    [PosixFilePath('/Volumes/release-90/variation/VEP/microtus_ochrogaster_vep_90_MicOch1.0.tar.gz'),
     PosixFilePath('/Volumes/release-90/variation/VEP/microtus_ochrogaster_refseq_vep_90_MicOch1.0.tar.gz'),
     PosixFilePath('/Volumes/release-90/variation/VEP/microtus_ochrogaster_merged_vep_90_MicOch1.0.tar.gz'),
     PosixFilePath('/Volumes/release-90/variation/VEP/microcebus_murinus_vep_90_Mmur_2.0.tar.gz'),
     PosixFilePath('/Volumes/release-90/rdf/microtus_ochrogaster/microtus_ochrogaster_xrefs.ttl.gz.graph'),


.. code:: python

    >>> path2insight.distance_on_token(filepaths[0:10]) 
    array([[ 0.        ,  2.        ,  1.41421356,  3.        ,  3.        ],
           [ 2.        ,  0.        ,  2.44948974,  3.31662479,  3.31662479],
           [ 1.41421356,  2.44948974,  0.        ,  3.        ,  3.        ],
           [ 3.        ,  3.31662479,  3.        ,  0.        ,  1.41421356],
           [ 3.        ,  3.31662479,  3.        ,  1.41421356,  0.        ]])


Installation and dependencies
=============================

Path2Insight is available on Pypi. This make it possible to install it with
through:

.. code:: bash

    pip install path2insight

To upgrade path2insight use 

.. code:: bash

    pip install --upgrade path2insight

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


Cite
====

Follows. 

Authors
=======

- Armel Lefebvre
- Jonathan de Bruin


