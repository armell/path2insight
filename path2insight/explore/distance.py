"""Submodule for computing similirity and distance between file paths."""

from __future__ import division

from path2insight.utils import PATH_OBJECT_TYPES
from path2insight.decorators import iter_advanced_2d
from path2insight.algorithms.stringdist import levenshtein as _levenshtein
from path2insight.algorithms.stringdist import levenshtein_normalised as _ln
from path2insight.tokenizers import DEFAULT_TOKENIZE_PATTERN


@iter_advanced_2d
def levenshtein_distance_stem(path1, path2=None, normalise=False):
    """String distance measure with Levenshtein.

    The Levenshtein distance between the stem of file paths. This function
    accepts list of WindowsFilePath and PosixFilePath objects. When the
    secodn argument is None, the distance of each path to each other is
    computed.

    :param path1: A list of filepath objects
    :type path1: list
    :param path2: A list of filepath objects. Default None.
    :type path2: list
    :param normalise: Normalise the Levenshtein distance. Default False.
    :type normalise: bool

    :Example:

    >>> from path2insight.explore import levenshtein_distance_stem
    >>> d = levenshtein_distance_stem(DATASET)

    :Note:

    1) This computation can be relativily heavy because it scales
    quadratically.

    2) For visual inspection, the `heatmap` function in seaborn can be
    useful.

    >>> sns.heatmap(d)

    """

    list1_str = [p1.stem for p1 in path1]
    if path2 is not None:
        list2_str = [p2.stem for p2 in path2]
    else:
        list2_str = None

    if normalise:
        result = _ln(list1_str, list2_str)
    else:
        result = _levenshtein(list1_str, list2_str)

    return result


def levenshtein_distance_tokens(path1, path2,
                                token_pattern=DEFAULT_TOKENIZE_PATTERN,
                                normalise=True, tagger=None):
    """Distance between path and list of tokens.

    :param path1: A WindowsFilePath or PosixFilePath or list of tokens.
    :type path1: WindowsFilePath, PosixFilePath
    :param path2: A WindowsFilePath or PosixFilePath or list of tokens
        to compare with.
    :type path2: WindowsFilePath, PosixFilePath
    :param token_pattern: A regular expression to use as tokeniser.
    :type token_pattern: str, regexp
    :param normalise: Normalise the Levenshtein distance. Default False.
    :type normalise: bool
    :param tagger: A Tagger object like `path2insight.BaseTypeTagger`.
        The minimum requirements for this tagger is a method named 'tag'
        that returns a list of tuples with structure (token, tag).
    :type tagger: object

    :returns: This function returns a tuple with structure: (list of lists,
        tokens_path, tokens_list). The first position is a matrix with all
        levenshtein distances.
    :return_type: tuple

    :Example:

    >>> m, tokens_path, tokens_input = levenshtein_distance_tokens(
            path, ["raw", "100mM", "F1"]
        )

    More advanced:

    >>> from path2insight.explore.tagger import TokenTypeTagger
    >>> # returns a tuple
    >>> m, tokens_path, tokens_input = levenshtein_distance_tokens(
    >>>     path, ["raw", "100mM", "F1"], tagger=TokenTypeTagger
    >>> )

    For pandas users:

    >>> pandas.DataFrame(m, index=tokens_input, columns=tokens_path)

    """

    if isinstance(path1, PATH_OBJECT_TYPES) and tagger:
        tagger_result1 = tagger().tag(path1)
        path_tokens1 = [token for token, tag in tagger_result1]
        path_tokens1_labels = tagger_result1
    elif isinstance(path1, PATH_OBJECT_TYPES):
        path_tokens1 = path1.tokenize(token_pattern=token_pattern)
        path_tokens1_labels = path_tokens1
    else:
        path_tokens1 = path1
        path_tokens1_labels = path1

    if isinstance(path2, PATH_OBJECT_TYPES) and tagger:
        tagger_result2 = tagger().tag(path2)
        path_tokens2 = [token for token, tag in tagger_result2]
        path_tokens2_labels = tagger_result2
    elif isinstance(path2, PATH_OBJECT_TYPES):
        path_tokens2 = path2.tokenize(token_pattern=token_pattern)
        path_tokens2_labels = path_tokens2
    else:
        path_tokens2 = path2
        path_tokens2_labels = path2

    # compute the distance matrix
    if normalise:
        lv = _ln(path_tokens1, path_tokens2)
    else:
        lv = _levenshtein(path_tokens1, path_tokens2)

    # return tuple with result
    return (lv, path_tokens2_labels, path_tokens1_labels)
