import pandas as pd
import numpy as np

import pytest

# seperated imports to prevent merge conflicts
from path2insight import WindowsFilePath, PosixFilePath
from path2insight.tests import TEST_PATHS_POSIX
from path2insight.tests import TEST_PATHS_WINDOWS
from path2insight.tests import TEST_PATHS_MULTI_WINDOWS
from path2insight.tests import TEST_PATHS_MULTI_POSIX
import path2insight


def test_parse_windows():

    fp_df = pd.DataFrame(TEST_PATHS_WINDOWS)
    fp_series = pd.Series(TEST_PATHS_WINDOWS)
    fp_np = np.array(TEST_PATHS_WINDOWS)
    fp_list = TEST_PATHS_WINDOWS

    result_df = path2insight.parse(fp_df, os_name='windows')
    result_series = path2insight.parse(fp_series, os_name='windows')
    result_np = path2insight.parse(fp_np, os_name='windows')
    result_list = path2insight.parse(fp_list, os_name='windows')

    assert all([isinstance(fp, WindowsFilePath) for fp in result_df])
    assert all([isinstance(fp, WindowsFilePath) for fp in result_series])
    assert all([isinstance(fp, WindowsFilePath) for fp in result_np])
    assert all([isinstance(fp, WindowsFilePath) for fp in result_list])

    assert result_df == result_series == result_np == result_list


def test_parse_posix():

    fp_df = pd.DataFrame(TEST_PATHS_POSIX)
    fp_series = pd.Series(TEST_PATHS_POSIX)
    fp_np = np.array(TEST_PATHS_POSIX)
    fp_list = TEST_PATHS_POSIX

    assert all([isinstance(fp, PosixFilePath)
                for fp in path2insight.parse(fp_df, os_name='posix')])
    assert all([isinstance(fp, PosixFilePath)
                for fp in path2insight.parse(fp_series, os_name='posix')])
    assert all([isinstance(fp, PosixFilePath)
                for fp in path2insight.parse(fp_np, os_name='posix')])
    assert all([isinstance(fp, PosixFilePath)
                for fp in path2insight.parse(fp_list, os_name='posix')])


@pytest.mark.parametrize("data", [
    pd.Series(TEST_PATHS_WINDOWS),
    pd.DataFrame(TEST_PATHS_WINDOWS),
    pd.DataFrame(TEST_PATHS_MULTI_WINDOWS)
])
def test_from_pandas_windows(data):

    result = path2insight.parse_from_pandas(data, 'windows')

    # the result is a list
    assert isinstance(result, list)

    # each element in the list is a WindowsFilePath
    assert all([isinstance(fp, WindowsFilePath) for fp in result])


@pytest.mark.parametrize("data", [
    pd.Series(TEST_PATHS_POSIX),
    pd.DataFrame(TEST_PATHS_POSIX),
    pd.DataFrame(TEST_PATHS_MULTI_POSIX)
])
def test_from_pandas_posix(data):

    result = path2insight.parse_from_pandas(data, 'posix')

    # the result is a list
    assert isinstance(result, list)

    # each element in the list is a PosixFilePath
    assert all([isinstance(fp, PosixFilePath) for fp in result])


@pytest.mark.parametrize("data", [
    np.array(TEST_PATHS_WINDOWS),
    np.array(TEST_PATHS_MULTI_WINDOWS)
])
def test_from_numpy_windows(data):

    result = path2insight.parse_from_numpy(data, 'windows')

    # the result is a list
    assert isinstance(result, list)

    # each element in the list is a WindowsFilePath
    assert all([isinstance(fp, WindowsFilePath) for fp in result])


@pytest.mark.parametrize("data", [
    np.array(TEST_PATHS_POSIX),
    np.array(TEST_PATHS_MULTI_POSIX)
])
def test_from_numpy_posix(data):

    result = path2insight.parse_from_numpy(data, 'posix')

    # the result is a list
    assert isinstance(result, list)

    # each element in the list is a PosixFilePath
    assert all([isinstance(fp, PosixFilePath) for fp in result])


@pytest.mark.parametrize("data", [
    TEST_PATHS_WINDOWS,
    TEST_PATHS_MULTI_WINDOWS
])
def test_from_list_windows(data):

    result = path2insight.parse_from_list(data, 'windows')

    # the result is a list
    assert isinstance(result, list)

    # each element in the list is a WindowsFilePath
    assert all([isinstance(fp, WindowsFilePath) for fp in result])


@pytest.mark.parametrize("data", [
    TEST_PATHS_POSIX,
    TEST_PATHS_MULTI_POSIX
])
def test_from_list_posix(data):

    result = path2insight.parse_from_list(data, 'posix')

    # the result is a list
    assert isinstance(result, list)

    # each element in the list is a PosixFilePath
    assert all([isinstance(fp, PosixFilePath) for fp in result])
