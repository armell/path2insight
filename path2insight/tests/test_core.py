import pytest

from path2insight import WindowsFilePath, PosixFilePath
from path2insight.tests import TEST_PATHS_POSIX, TEST_PATHS_WINDOWS


@pytest.mark.parametrize("filepath", TEST_PATHS_WINDOWS)
def test_type_windows(filepath):
    # test the type after initialization
    assert type(WindowsFilePath(filepath)) == WindowsFilePath

    # test the type after calling str
    assert type(str(WindowsFilePath(filepath))) == str

    # test the type of parent
    assert type(WindowsFilePath(filepath).parent) == WindowsFilePath

    # test the type of parents
    parents = WindowsFilePath(filepath).parents
    assert all([type(parent) == WindowsFilePath for parent in parents])


@pytest.mark.parametrize("filepath", TEST_PATHS_POSIX)
def test_type_posix(filepath):
    # test the type after initialization
    assert type(PosixFilePath(filepath)) == PosixFilePath

    # test the type after calling str
    assert type(str(PosixFilePath(filepath))) == str

    # test the type of parent
    assert type(PosixFilePath(filepath).parent) == PosixFilePath

    # test the type of parents
    parents = PosixFilePath(filepath).parents
    assert all([type(parent) == PosixFilePath for parent in parents])


@pytest.mark.parametrize("filepath", TEST_PATHS_WINDOWS)
def test_args_windows(filepath):
    # test the args after calling
    assert WindowsFilePath(filepath).args == filepath


@pytest.mark.parametrize("filepath", TEST_PATHS_POSIX)
def test_args_posix(filepath):
    # test the args after calling
    assert PosixFilePath(filepath).args == filepath


def test_string_methods_path_windows():
    filename = 'C:/Program Files/unittest/DOCS.pdf'
    expected_lower = 'c://program files/unittest/docs.pdf'
    expected_title = 'C:/Program Files/Unittest/Docs.Pdf'

    assert str(WindowsFilePath(filename).lower()) == \
        str(WindowsFilePath(expected_lower))

    assert str(WindowsFilePath(filename).title()) == \
        str(WindowsFilePath(expected_title))

    # print(WindowsFilePath(filename).islower())
    # assert WindowsFilePath(filename).islower() == [False, False, True, False]


def test_string_methods_name_windows():
    filename = 'C:/Program Files/unittest/DOCS.pdf'
    expected_lower = 'C:/Program Files/unittest/docs.pdf'
    expected_title = 'C:/Program Files/unittest/Docs.Pdf'

    assert str(WindowsFilePath(filename).lower_name()) == \
        str(WindowsFilePath(expected_lower))

    assert str(WindowsFilePath(filename).title_name()) == \
        str(WindowsFilePath(expected_title))

    assert WindowsFilePath(filename).islower_name() is False

    assert WindowsFilePath(filename).isupper_name() is False

    assert WindowsFilePath(filename).index_name("O") == 1


def test_string_methods_stem_windows():
    filename = 'C:/Program Files/unittest/DOCS.pdf'
    expected_lower = 'C:/Program Files/unittest/docs.pdf'
    expected_title = 'C:/Program Files/unittest/Docs.pdf'
    expected_upper = 'C:/Program Files/unittest/DOCS.pdf'

    assert str(WindowsFilePath(filename).lower_stem()) == \
        str(WindowsFilePath(expected_lower))

    assert str(WindowsFilePath(filename).title_stem()) == \
        str(WindowsFilePath(expected_title))

    assert str(WindowsFilePath(filename).upper_stem()) == \
        str(WindowsFilePath(expected_upper))

    assert WindowsFilePath(filename).islower_stem() is False

    assert WindowsFilePath(filename).isupper_stem() is True

    assert WindowsFilePath(filename).index_stem("O") == 1


def test_string_methods_listof_windows():
    filenames = [WindowsFilePath('C:/Program Files/unittest/DOCS1.pdf'),
                 WindowsFilePath('C:/Program Files/unittest/DOCS2.pdf')]
    expected_lower = [WindowsFilePath('C:/Program Files/unittest/docs1.pdf'),
                      WindowsFilePath('C:/Program Files/unittest/docs2.pdf')]

    result = [fp.lower_name() for fp in filenames]

    assert result[0] == expected_lower[0]
    assert result[0] != expected_lower[1]
    assert result[1] != expected_lower[0]
    assert result[1] == expected_lower[1]


def test_string_extension_prop():
    filename_single_ext = 'C:/Program Files/unittest/DOCS.pdf'
    filename_multiple_ext = 'C:/Program Files/unittest/DOCS.pdf.tar'

    assert WindowsFilePath(filename_single_ext).extension == \
        WindowsFilePath(filename_single_ext).suffix

    assert WindowsFilePath(filename_multiple_ext).extension == \
        WindowsFilePath(filename_multiple_ext).suffix


def test_tokenize_name():
    filename = 'C:/Program Files/unittest/DOCS_11Mar2020-Armel final.pdf'

    assert WindowsFilePath(filename).tokenize_stem() == \
        ['DOCS', '11Mar2020', 'Armel', 'final']

    assert WindowsFilePath(filename).tokenize_name() == \
        ['DOCS', '11Mar2020', 'Armel', 'final', 'pdf']


def test_tokenize():
    filename = 'C:/Program Files/unittest/DOCS_11Mar2020-Armel final.pdf'

    assert WindowsFilePath(filename).tokenize() == \
        ['C:', 'Program', 'Files', 'unittest',
         'DOCS', '11Mar2020', 'Armel', 'final']

    assert WindowsFilePath(filename).tokenize(
        exclude_extension=False) == \
        ['C:', 'Program', 'Files', 'unittest',
         'DOCS', '11Mar2020', 'Armel', 'final', 'pdf']


def test_depth():
    filename = 'C:/Program Files/unittest/DOCS_11Mar2020-Armel final.pdf'

    assert WindowsFilePath(filename).depth == 3
