import sys

from path2insight.core import WindowsFilePath, PosixFilePath
from path2insight.parse import *
from path2insight.collect import *
from path2insight.handling import *
from path2insight.explore import *
from path2insight.external.nltk import (ngrams,
                                        bigrams,
                                        trigrams,
                                        everygrams,
                                        skipgrams)

__all__ = [
    'tokenizers', 'datasets'
]

__version__ = "1.0b2"
