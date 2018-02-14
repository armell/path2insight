# seperated imports to prevent merge conflicts
from path2insight import WindowsFilePath
import path2insight


def test_select():

    data = [WindowsFilePath("F:/data/file.txt"),
            WindowsFilePath("F:/docs/file.xlsx"),
            WindowsFilePath("F:/test/file.demo"),
            WindowsFilePath("F:/README.txt")]

    result = path2insight.select(data, level1='data')
    expected = [WindowsFilePath("F:/data/file.txt")]

    assert result == expected


def test_select_wildcard():

    data = [WindowsFilePath("F:/data/file.txt"),
            WindowsFilePath("F:/docs/file.xlsx"),
            WindowsFilePath("F:/test/file.demo"),
            WindowsFilePath("F:/README.txt")]

    # * notation
    result = path2insight.select(data, level2='*')
    expected = [WindowsFilePath("F:/data/file.txt"),
                WindowsFilePath("F:/docs/file.xlsx"),
                WindowsFilePath("F:/test/file.demo")]

    assert result == expected

    # same different notation
    result = path2insight.select(data, level2=True)

    assert result == expected


def test_select_re():

    data = [WindowsFilePath("F:/data/file.txt"),
            WindowsFilePath("F:/docs/file.xlsx"),
            WindowsFilePath("F:/test/file.demo"),
            WindowsFilePath("F:/README.txt")]

    result = path2insight.select_re(data, level1=r"[A-Z]")
    expected = [WindowsFilePath("F:/README.txt")]

    assert result == expected

    result = path2insight.select_re(data, level1=r"^d")
    expected = [WindowsFilePath("F:/data/file.txt"),
                WindowsFilePath("F:/docs/file.xlsx")]

    assert result == expected
