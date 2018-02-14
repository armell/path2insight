import path2insight
from path2insight.datasets import load_ensembl, load_pride


def test_load_ensembl():

    N = 100

    data = load_ensembl(nrows=N)

    # test the instance type
    assert isinstance(data, list)

    # check the length
    assert len(data) == N

    # check each value
    assert all([type(fp) == path2insight.PosixFilePath for fp in data])


def test_load_pride():

    N = 100

    data = load_pride(nrows=N)

    # test the instance type
    assert isinstance(data, list)

    # check the length
    assert len(data) == N

    # check each value
    assert all([type(fp) == path2insight.PosixFilePath for fp in data])
