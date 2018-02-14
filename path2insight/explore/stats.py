from __future__ import division

from collections import Counter
from itertools import chain

from path2insight.utils import is_list_like, MissingDependencyError
from path2insight.tokenizers import default_tokenizer

"""Module to count observations and do statistics."""


def similar_records(record, ref_set):
    raise NotImplementedError()


def _normalize_counter(c):
    """Normalize the values of a counter"""

    total = sum(c.values())
    for key in c:
        c[key] /= total

    return c


def depth_counts(x, normalize=False, center=None):
    """Count the filepath-depths.

    This function counts the filepath depths of a list of filepaths. The
    function returns a Python :py:class:`collections.Counter` object. This
    Counter object can be used to compute the most common depths or substract
    other Counter objects. For all options, see the Python documentation.

    :param x: Paths to determine the depth of.
    :type x: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param normalize: Normalize the Counter result. Default False.
    :type normalize: bool
    :param center: Method to correct the offset of the data. Options are
        'mean' or callable. Default None.
    :type center: str, NoneType, callable

    :return: filepath depths counted
    :rtype: collections.Counter

    :Example:

    >>> path2insight.depth_counts(list_of_filepaths)
    Counter({5: 32, 6: 654, 7: 284, 8: 13, 9: 11, 10: 1, 11: 4, 13: 1})

    :Note:

    To get a Python :py:class:`dict`, simply wrap the Counter object with
    :code:`dict()`.

    """

    if not is_list_like(x):
        raise TypeError('expected list-like object')

    data_depth = [fp.depth for fp in x]

    # start correction for center
    if center == 'mean':
        offset = int(sum(data_depth) / len(data_depth))
        data_depth = [d - offset for d in data_depth]
    elif callable(center):
        offset = center(data_depth)
        data_depth = [d - offset for d in data_depth]
    elif not center:
        pass
    else:
        raise Exception("Unknown value for 'center'")
    # end correlation for center

    c = Counter(data_depth)

    if normalize:
        c = _normalize_counter(c)

    return c


def n_extension_counts(x):
    """[CHANGE FUNCTION NAME]Count the number of extensions."""

    return Counter([len(fp.suffixes) for fp in x])


def extension_counts(x, lower=False, normalize=False):
    """Count the extensions of the filenames.

    This function counts the name extensions of a list of filepaths. The
    function returns a Python :py:class:`collections.Counter` object. This
    Counter object can be used to compute the most common extensions or
    substract other Counter objects. For all options, see the Python
    documentation.

    :param x: Paths to determine the extension count of.
    :type x: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param lower: Convert the extensions to lower before counting.
    :type lower: boolean
    :param normalize: Normalize the Counter result. Default False.
    :type normalize: bool

    :return: extensions counted
    :rtype: collections.Counter

    :Example:

    >>> path2insight.extension_counts(filepaths_list)
    Counter({'.zip': 42, '.raw': 3, '.txt': 12, '.docx': 1})
    >>> path2insight.extension_counts(filepaths_list).most_common(3)
    [('.zip', 42), ('.txt', 12), ('.raw', 3)]

    :Note:

    To get a Python :py:class:`dict`, simply wrap the Counter object with
    :code:`dict()`.

    """

    if lower:
        res = [fp.suffix.lower() for fp in x]
    else:
        res = [fp.suffix for fp in x]

    c = Counter(res)

    if normalize:
        c = _normalize_counter(c)

    return c


def name_counts(x, lower=False, normalize=False):
    """Count the names.

    This function counts the names of a list of filepaths. The function
    returns a Python :py:class:`collections.Counter` object. This Counter
    object can be used to compute the most common names or substract other
    Counter objects. For all options, see the Python documentation.

    :param x: Paths to count the names of.
    :type x: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param lower: Convert the filenames to lower before counting.
    :type lower: boolean
    :param normalize: Normalize the Counter result. Default False.
    :type normalize: bool

    :return: names counted
    :rtype: collections.Counter

    :Note:

    To get a Python :py:class:`dict`, simply wrap the Counter object with
    :code:`dict()`.

    """

    if lower:
        res = [fp.name.lower() for fp in x]
    else:
        res = [fp.name for fp in x]

    c = Counter(res)

    if normalize:
        c = _normalize_counter(c)

    return c


def stem_counts(x, lower=False, normalize=False):
    """Count the stems.

    This function counts the stems of a list of filepaths. The function
    returns a Python :py:class:`collections.Counter` object. This Counter
    object can be used to compute the most common stems or substract other
    Counter objects. For all options, see the Python documentation.

    :param x: Paths to count the stems of.
    :type x: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param lower: Convert the stems to lower before counting.
    :type lower: boolean
    :param normalize: Normalize the Counter result. Default False.
    :type normalize: bool

    :return: stems counted
    :rtype: collections.Counter

    :Note:

    To get a Python :py:class:`dict`, simply wrap the Counter object with
    :code:`dict()`.

    """

    if lower:
        res = [fp.stem.lower() for fp in x]
    else:
        res = [fp.stem for fp in x]

    c = Counter(res)

    if normalize:
        c = _normalize_counter(c)

    return c


def drive_counts(x, lower=False, normalize=False):
    """Count the drives of the paths.

    This function counts the drives of a list of filepaths. The function
    returns a Python :py:class:`collections.Counter` object. This Counter
    object can be used to compute the most common drives or substract other
    Counter objects. For all options, see the Python documentation.

    :param x: Paths to count the stems of.
    :type x: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param lower: Convert the drive to lower before counting.
    :type lower: boolean
    :param normalize: Normalize the Counter result. Default False.
    :type normalize: bool

    :return: drives counted
    :rtype: collections.Counter

    :Note:

    To get a Python :py:class:`dict`, simply wrap the Counter object with
    :code:`dict()`.

    """

    if lower:
        res = [fp.drive.lower() for fp in x]
    else:
        res = [fp.drive for fp in x]

    c = Counter(res)

    if normalize:
        c = _normalize_counter(c)

    return c


def token_counts(x, tokenizer=default_tokenizer, lower=False,
                 parents=False, stem=True, extension=False, normalize=False):
    """Count the tokens in the paths.

    This function counts the tokens of a list of filepaths. Use boolean
    settings to include the parents, stem and extension. The function returns
    a Python :py:class:`collections.Counter` object. This Counter object can
    be used to compute the most common tokens or substract other Counter
    objects. For all options, see the Python documentation.

    :param x: Paths to count the stems of.
    :type x: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param parents: tokenize the parents
    :type parents: bool
    :param stem: tokenize the stem
    :type stem: bool
    :param extension: tokenisze the extension
    :type extension: bool
    :param lower: Convert the filepath to lower before counting.
    :type lower: boolean
    :param normalize: Normalize the Counter result. Default False.
    :type normalize: bool

    :return: drives counted
    :rtype: collections.Counter

    :Example:

    >>> path2insight.token_counts(data).most_common(3)
    [('FUNC001', 288), ('LTQ', 173), ('FUNCTNS', 96)]

    :Note:

    To get a Python :py:class:`dict`, simply wrap the Counter object with
    :code:`dict()`.

    """

    res = [fp.lower() for fp in x] if lower else [fp for fp in x]

    if not parents and stem and not extension:
        res = [fp.tokenize_stem() for fp in res]
    elif parents and stem and extension:
        res = [fp.tokenize() for fp in res]
    elif not parents and stem and extension:
        res = [fp.tokenize_name() for fp in res]
    else:
        raise NotImplementedError('this combination is not implemented yet')

    flat_res = list(chain.from_iterable(res))

    c = Counter(flat_res)

    if normalize:
        c = _normalize_counter(c)

    return c


def extension_chisquare(x, y=None, lower=True):
    """Calculates a one-way chi square test for file extensions.

    :param x: Paths to compare with y.
    :type x: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param y: Paths to compare with x.
    :type y: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param lower: Convert the extensions to lower before counting.
    :type lower: boolean

    :return: The test result.
    :rtype: scipy.stats.Power_divergenceResult

    """

    try:
        from scipy.stats import chisquare
        from sklearn.feature_extraction import DictVectorizer
    except ModuleNotFoundError:
        raise MissingDependencyError(
            "Install the module 'scipy' and 'sklearn' to compute chisquares.")

    counts_x = extension_counts(x, lower=lower)
    counts_y = extension_counts(y, lower=lower)

    dv = DictVectorizer(sparse=False)
    arr = dv.fit_transform([counts_x, counts_y])
    return chisquare(arr[0], arr[1])


def name_chisquare(x, y=None, lower=True):
    """Calculates a one-way chi square test for file names.

    :param x: Paths to compare with y.
    :type x: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param y: Paths to compare with x.
    :type y: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param lower: Convert the extensions to lower before counting.
    :type lower: boolean

    :return: The test result.
    :rtype: scipy.stats.Power_divergenceResult

    """

    try:
        from scipy.stats import chisquare
        from sklearn.feature_extraction import DictVectorizer
    except ModuleNotFoundError:
        raise MissingDependencyError(
            "Install the module 'scipy' and 'sklearn' to compute chisquares.")

    counts_x = name_counts(x, lower=lower)
    counts_y = name_counts(y, lower=lower)

    dv = DictVectorizer(sparse=False)
    arr = dv.fit_transform([counts_x, counts_y])
    return chisquare(arr[0], arr[1])


def stem_chisquare(x, y=None, lower=True):
    """Calculates a one-way chi square test for file name stems.

    :param x: Paths to compare with y.
    :type x: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param y: Paths to compare with x.
    :type y: list, tuple, array of WindowsFilePath or PosixFilePath objects
    :param lower: Convert the extensions to lower before counting.
    :type lower: boolean

    :return: The test result.
    :rtype: scipy.stats.Power_divergenceResult

    """

    try:
        from scipy.stats import chisquare
        from sklearn.feature_extraction import DictVectorizer
    except ModuleNotFoundError:
        raise MissingDependencyError(
            "Install the module 'scipy' and 'sklearn' to compute chisquares.")

    counts_x = stem_counts(x, lower=lower)
    counts_y = stem_counts(y, lower=lower)

    dv = DictVectorizer(sparse=False)
    arr = dv.fit_transform([counts_x, counts_y])
    return chisquare(arr[0], arr[1])
