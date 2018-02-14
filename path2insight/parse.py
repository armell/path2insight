from path2insight import WindowsFilePath, PosixFilePath


def parse(obj, os_name=None):
    """Parse (list of) file paths.

    Parse a list with file paths into list of WindowsFilePath
    and PosixFilePath objects. This function can parse list, tuple,
    numpy.ndarray and pandas.Series. This is done with one of the following
    parsers: parse_from_pandas, parse_from_numpy or parse_from_list.

    :Example:

    >>> data = ['file1.xml', 'data/file1.txt', 'data/file2.txt']
    >>> path2insight.parse(data, os_name='windows')

    gives the same result as

    >>> import pandas
    >>> path2insight.parse(pandas.Series(data), os_name='windows')

    :param obj: An object such as a list, numpy array or pandas.Series
        with filepaths in the form of strings.
    :type obj: list, tuple, numpy.ndarray, pandas.Series
    :param os_name: The operation system on with the filepaths are collected.
        The options are 'windows' or 'posix' for Windows and Posix system
        repectivily.
    :type os_name: str

    :return: Returns a list with WindowsFilePaths and PosixFilePaths.
    :return_type: list

    """

    # try for a list or tuple
    if isinstance(obj, (list, tuple)):
        return parse_from_list(obj, os_name=os_name)

    # try for numpy object
    try:
        return parse_from_numpy(obj, os_name=os_name)
    except (ImportError, TypeError):
        pass

    # try for pandas object
    try:
        return parse_from_pandas(obj, os_name=os_name)
    except (ImportError, TypeError):
        pass

    # none of the above were succesfull
    raise TypeError("failed to parse object")


def parse_from_pandas(pandas_object, os_name=None):
    """Parse a series or dataframe with file paths.

    See :py:func:`path2insight.parse` for additional information.

    :param obj: An pandas.Series or pandas.DataFrame with filepaths in the
        form of strings.
    :type obj: pandas.Series or pandas.DataFrame
    :param os_name: The operation system on with the filepaths are collected.
        The options are 'windows' or 'posix' for Windows and Posix system
        repectivily.
    :type os_name: str

    :return: Returns a list with WindowsFilePaths and PosixFilePaths.
    :return_type: list
    """

    try:
        import pandas as pd
    except ImportError:
        raise ImportError('pandas is required for this function')

    if not isinstance(pandas_object, (pd.Series, pd.DataFrame)):
        raise TypeError('expected pandas.DataFrame of pandas.Series object')

    if os_name in ['windows', 'nt']:
        FilePathObject = WindowsFilePath
    elif os_name in ['posix', 'linux']:
        FilePathObject = PosixFilePath
    else:
        raise ValueError('incorrect os_name given')

    if isinstance(pandas_object, pd.DataFrame):
        pandas_list = list(pandas_object.itertuples(index=False, name=None))
        return [FilePathObject(*fp) for fp in pandas_list]
    else:
        pandas_list = pandas_object.tolist()
        return [FilePathObject(fp) for fp in pandas_list]


def parse_from_numpy(np_object, os_name=None):
    """Parse a numpy array with file paths.

    See :py:func:`path2insight.parse` for additional information.

    :param obj: A numpy.ndarray with filepaths in the form of strings.
    :type obj: numpy.ndarray
    :param os_name: The operation system on with the filepaths are collected.
        The options are 'windows' or 'posix' for Windows and Posix system
        repectivily.
    :type os_name: str

    :return: Returns a list with WindowsFilePaths and PosixFilePaths.
    :return_type: list
    """

    try:
        import numpy as np
    except ImportError:
        raise ImportError('numpy is required for this function')

    if not isinstance(np_object, (np.ndarray)):
        raise TypeError('expected np.ndarray object')

    if os_name in ['windows', 'nt']:
        FilePathObject = WindowsFilePath
    elif os_name in ['posix', 'linux']:
        FilePathObject = PosixFilePath
    else:
        raise ValueError('incorrect os_name given')

    if isinstance(np_object, np.ndarray) and len(np_object.shape) > 1:
        return [FilePathObject(*tuple(fp)) for fp in np_object.tolist()]
    else:
        return [FilePathObject(fp) for fp in np_object.tolist()]


def parse_from_list(l, os_name=None):
    """Parse a list with file paths.

    See :py:func:`path2insight.parse` for additional information.

    :param obj: A list with filepaths in the form of strings.
    :type obj: list
    :param os_name: The operation system on with the filepaths are collected.
        The options are 'windows' or 'posix' for Windows and Posix system
        repectivily.
    :type os_name: str

    :return: Returns a list with WindowsFilePaths and PosixFilePaths.
    :return_type: list
    """

    if os_name in ['windows', 'nt']:
        FilePathObject = WindowsFilePath
    elif os_name in ['posix', 'linux']:
        FilePathObject = PosixFilePath
    else:
        raise ValueError('incorrect os_name given')

    if not isinstance(l, (list, tuple)):
        raise ValueError('expect a list with filepaths')

    l_args = map(lambda x: tuple(x) if isinstance(
        x, (tuple, list)) else tuple([x]), l)

    return [FilePathObject(*fp) for fp in l_args]
