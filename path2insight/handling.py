import re
import random
import warnings

from functools import partial

from path2insight.utils import VisibleDeprecationWarning


def subset(*args, **kwargs):
    """[DEPRECATED] This function is replaced by select()"""

    warnings.warn(
        "This function is deprecated. Use select() instead of subset()",
        VisibleDeprecationWarning
    )

    return filter(*args, **kwargs)


def _match_file_path(path, level, v):
    """Helper function to match part."""

    if v == "*" or v is True:
        try:
            path[level]
            return True
        except IndexError:
            return False
    else:
        return path[level] == v


def _re_match_file_path(path, level, v):
    """Helper function to match part with regexp pattern."""

    try:
        if re.match(v, path[level]):
            return True
        else:
            return False
    except IndexError:
        return False


def select(paths, **kwargs):
    """Select from a list of filepaths.

    This function selects from a list of filepaths based on their
    part (like folder of file) names. This is done with the
    level arguments.

    :param paths: A list of filepaths
    :type paths: list
    :param level0: The value(s) of the first level (root).
    :type level0: (list of) str
    :param level1:  The value(s) of the second level.
    :type level1: (list of) str
    :param level*:  The value(s) of the nth level.
    :type level*: (list of) str

    :return: A list with the selection of matching filepath.
    :return_type: list

    :Note:

    One can use the value "*" to select all file paths. If a file path
    doesn't have a value on that level (because the level is higher
    than the number of parts), then the path is excluded from the
    selection. One can also use `True` instead of "*".

    :Example:

    Selection based on the name of a level.

    >>> import path2insight
    >>> data = [path2insight.WindowsFilePath("F:/data/file.txt"),
                path2insight.WindowsFilePath("F:/docs/file.xlsx"),
                path2insight.WindowsFilePath("F:/test/file.demo"),
                path2insight.WindowsFilePath("F:/README.txt")]
    >>> path2insight.select(data, level1='data')
    [path2insight.WindowsFilePath("F:/data/file.txt")]

    Selection based on the existence of a level (wilcard). Path is
    only included when level exists.

    >>> path2insight.select(data, level2='*')
    [path2insight.WindowsFilePath("F:/data/file.txt"),
     path2insight.WindowsFilePath("F:/docs/file.xlsx"),
     path2insight.WindowsFilePath("F:/test/file.demo")]

    """

    kwargs['regexp'] = False

    return _select(paths, **kwargs)


def select_re(paths, **kwargs):
    """Select from a list of filepaths.

    This function selects from a list of filepaths based on their
    part (like folder of file) names. This is done with the
    level arguments.

    :param paths: A list of filepaths
    :type paths: list
    :param level0: The value(s) of the first level (root).
    :type level0: (list of) str
    :param level1:  The value(s) of the second level.
    :type level1: (list of) str
    :param level*:  The value(s) of the nth level.
    :type level*: (list of) str

    :return: A list with the selection of matching filepath.
    :return_type: list

    :Example:

    Selection based on the name of a level.

    >>> import path2insight
    >>> data = [path2insight.WindowsFilePath("F:/data/file.txt"),
                path2insight.WindowsFilePath("F:/docs/file.xlsx"),
                path2insight.WindowsFilePath("F:/test/file.demo"),
                path2insight.WindowsFilePath("F:/README.txt")]
    >>> path2insight.select(data, level1=r"[A-Z]")
    [path2insight.WindowsFilePath("F:/README.txt")]

    Select all paths starting with the letter d on the first level.

    >>> path2insight.select(data, level1=r"^d")
    [path2insight.WindowsFilePath("F:/data/file.txt"),
     path2insight.WindowsFilePath("F:/docs/file.xlsx")]

    """

    kwargs['regexp'] = True

    return _select(paths, **kwargs)


def _select(paths, **kwargs):

    use_re = kwargs.pop('regexp')

    matcher = _re_match_file_path if use_re else _match_file_path

    levels = []

    for level, value in kwargs.items():
        match = re.match(r"level([0-9]+)", level)
        if match:
            levels.append((int(match.group(1)), value))
        else:
            raise TypeError(
                "{} is an invalid keyword argument for this function"
                .format(level))

    data_selection = paths
    for level, value in levels:
        if not isinstance(value, (list, tuple)):
            value = [value]

        data_temp = []
        for path in data_selection:
            try:
                if any([matcher(path.parts, level, v) for v in value]):
                    data_temp.append(path)
            except IndexError:
                pass
        data_selection = data_temp
        data_temp = []

    return data_selection


def sort(paths, level=None, reverse=False):
    """Sort a list of filepaths.

    This function sorts a list of filepaths. The sorting can be
    based on parts of the (like folder of file) names. This is done
    with the key arguments.

    :param paths: A list of filepaths
    :type paths: list
    :param level: List of positions which refer to the axis items.
        Default None.
    :type level: (list of) int
    :param reverse:  Reverse the sort.
    :type reverse: bool

    :return: A sorted list.
    :return_type: list

    :Example:

    >>> path2insight.sort(data)
    >>> path2insight.sort(data, key=1)
    >>> path2insight.sort(data, key=1, reverse=True)
    >>> path2insight.sort(data, key=[5, 4])

    """

    def _key_sort(x, level):

        a = []
        for k in level:
            try:
                a.append(x.parts[k])
            except IndexError:
                pass

        return a

    data_copy = paths.copy()

    if level is not None:
        if not isinstance(level, (list, tuple)):
            level = [level]
        data_copy.sort(key=partial(_key_sort, level=level), reverse=reverse)
    else:
        data_copy.sort(reverse=reverse)

    return data_copy


def sample(data, n=None):
    """Take a random sample of filepaths.

    :param paths: A list of filepaths
    :type paths: list
    :param n: The number of filepaths to return. If None, all filepaths are
        returned in a random order. Default None.
    :type n: int, optional

    :return: A list with a sample of filepath.
    :return_type: list

    """

    if n is not None:
        return random.sample(data, n)
    else:
        data_copy = data.copy()
        random.shuffle(data_copy)
        return data_copy
