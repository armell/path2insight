import sys

from collections import Iterable

from path2insight import WindowsFilePath, PosixFilePath

PATH_OBJECT_TYPES = (WindowsFilePath, PosixFilePath)


# ----------------------------------------------------

class VisibleDeprecationWarning(UserWarning):
    """Visible deprecation warning.
    Based on numpy's VisibleDeprecationWarning.
    """
    pass


def MissingDependencyError(Exception):
    """Optional dependency not available."""

    pass


def _import_jellyfish():
    """Check if jellyfish is installed."""

    try:
        from jellyfish import levenshtein_distance as lv
        return lv
    except ModuleNotFoundError:
        raise MissingDependencyError(
            "Install the module 'jellyfish' to compute string distances.")


def iteritems(d):
    """Python 2, 3 compatibility."""
    try:
        return d.items()
    except AttributeError:
        return d.iteritems()


def unique(l):
    """Return a list with unique elements"""
    return list(set(l))


# ----------------------------------------------------
# the following path is largely based / taken from the six module and pandas

PY3 = (sys.version_info[0] >= 3)

if PY3:
    string_types = str,
    binary_type = bytes
else:
    string_types = basestring,
    binary_type = str


string_and_binary_types = (string_types,) + (binary_type,)


def is_list_like(obj):
    """
    Check if the object is list-like.
    Objects that are considered list-like are for example Python
    lists, tuples, sets, NumPy arrays, and Pandas Series.
    Strings and datetime objects, however, are not considered list-like.
    Parameters
    ----------
    obj : The object to check.
    Returns
    -------
    is_list_like : bool
        Whether `obj` has list-like properties.
    Examples
    --------
    >>> is_list_like([1, 2, 3])
    True
    >>> is_list_like({1, 2, 3})
    True
    >>> is_list_like(datetime(2017, 1, 1))
    False
    >>> is_list_like("foo")
    False
    >>> is_list_like(1)
    False
    """

    return (isinstance(obj, Iterable) and
            not isinstance(obj, string_types + (binary_type,)))

