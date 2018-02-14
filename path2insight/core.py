import re
from functools import partial
from itertools import chain

try:
    # python 3
    from pathlib import PurePath as _PurePath
    from pathlib import _windows_flavour, _posix_flavour
except ImportError:
    # python 2
    from pathlib2 import PurePath as _PurePath
    from pathlib2 import _windows_flavour, _posix_flavour

from path2insight.tokenizers import tokenizer, DEFAULT_TOKENIZE_PATTERN


class _FilePath(_PurePath):
    """Base object to analyse file or folder path.
    """

    _flavour = None

    def __init__(self, *args):
        super(_FilePath, self).__init__()

        # the raw argument or arguments
        if len(args) == 1:
            self.args = args[0]
        else:
            self.args = args

    @property
    def extension(self):
        """Masked property from self.suffix"""

        return self.suffix

    @property
    def extensions(self):
        """Masked property from self.suffixes"""

        return self.suffixes

    def tokenize_stem(self, token_pattern=DEFAULT_TOKENIZE_PATTERN):
        """Tokenise the name"""

        return tokenizer(self.stem, token_pattern)

    def tokenize_name(self, token_pattern=DEFAULT_TOKENIZE_PATTERN):
        """Tokenise the name"""

        return tokenizer(self.name, token_pattern)

    def tokenize(self, token_pattern=DEFAULT_TOKENIZE_PATTERN,
                 exclude_extension=True):
        """Tokenise the name (without extension)"""

        if exclude_extension:
            i = self._parts[-1].find('.')
            if 0 < i < len(self._parts[-1]) - 1:
                last_part = self._parts[-1][:i]
            else:
                last_part = ''
        else:
            last_part = self._parts[-1]

        parts = self._parts[:-1] + [last_part]

        return list(chain.from_iterable(
            [tokenizer(part, token_pattern) for part in parts]
        ))

    @property
    def depth(self):
        """Compute the depth of the path.

        :Example:

        >>> WindowsFilePath('R:/Armel/path2insight/demo.py').depth
        3

        """

        depth = len(self._parts)

        if depth > 1:
            return depth - 1
        else:
            return 0

    def clean_name(self, inplace=False):
        raise NotImplementedError()


def apply_str_method_to_filepath(str_method):

    def _string_filepath(self, *args, **kwargs):
        """Add string methods to _FilePath methods."""

        return self._from_parsed_parts(

            # drive
            getattr(self._drv, str_method)(*args, **kwargs),

            # root
            getattr(self._root, str_method)(*args, **kwargs),

            # parts and file extension
            [getattr(part, str_method)(*args, **kwargs)
             for part in self._parts]
        )

    docstring_fp = "Apply string function '{}' to filename parts."
    _string_filepath.__doc__ = docstring_fp.format(str_method)

    return _string_filepath


def apply_str_method_to_name(str_method):

    def _string_name(self, *args, **kwargs):
        """Add string methods to _FilePath methods (only filenames)."""

        new_name = getattr(self._parts[-1], str_method)(*args, **kwargs)

        if isinstance(new_name, str):

            return self._from_parsed_parts(

                # drive
                self._drv,

                # root
                self._root,

                # parts and file extension
                self._parts[:-1] + [new_name]
            )
        else:
            return new_name

    docstring_fn = "Apply string function '{}' to the name."
    _string_name.__doc__ = docstring_fn.format(str_method)

    return _string_name


def apply_str_method_to_stem(str_method):
    def _string_stem(self, *args, **kwargs):
        """Add string methods to _FilePath methods (only filenames)."""

        new_stem = getattr(self.stem, str_method)(*args, **kwargs)

        if isinstance(new_stem, str):

            return self._from_parsed_parts(

                # drive
                self._drv,

                # root
                self._root,

                # parts and file extension
                self._parts[:-1] + [new_stem + self.suffix]
            )
        else:
            return new_stem

    docstring_stem = "Apply string function '{}' to the stem."
    _string_stem.__doc__ = docstring_stem.format(str_method)

    return _string_stem


# set all the public string methods
str_methods = [method_name for method_name in dir(str)
               if not method_name.startswith("_")]

for str_method in str_methods:

    # file path string operations
    setattr(_FilePath, str_method,
            apply_str_method_to_filepath(str_method))

    # file name string operations
    setattr(_FilePath, "{}_name".format(str_method),
            apply_str_method_to_name(str_method))

    # file name string operations
    setattr(_FilePath, "{}_stem".format(str_method),
            apply_str_method_to_stem(str_method))


class WindowsFilePath(_FilePath):
    """Object to analyse Windows file or folder path.

    The WindowsFilePath inherits from :py:class:`pathlib.PureWindowsPath` in
    Python >3.4. See the documentation for all properties and methods.

    Examples:

    >>> p = WindowsFilePath("D://Documents/ProjectX/DEMO code.py")
    >>> str(p)
    'D:\\Documents\\ProjectX\\DEMO code.py'
    >>> p.lower_name().tokenize_stem()
    ['demo', 'code']
    >>> p.extension
    '.py'

    .. seealso::

        https://docs.python.org/3/library/pathlib.html#methods-and-properties

    """

    _flavour = _windows_flavour


class PosixFilePath(_FilePath):
    """Object to analyse Posix file or folder path.

    The WindowsFilePath inherits from pathlib.PureWindowsPath in Python >3.4.
    See https://docs.python.org/3/library/pathlib.html#methods-and-properties
    for all properties and methods.

    """

    _flavour = _posix_flavour
