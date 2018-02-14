import re

DEFAULT_TOKENIZE_PATTERN = r"(?u)([a-zA-Z0-9\:]+)(?=[^a-zA-Z0-9\:]|$)"
DEFAULT_PATH_SPLIT_PATTERN = r"[\\\/]+"
DEFAULT_CAMEL_SPLIT_PATTERN = None
DEFAULT_TITLE_SPLIT_PATTERN = None


def tokenizer(x, token_pattern):
    return re.findall(token_pattern, x, re.UNICODE)


def splitter(x, split_pattern):
    return re.split(split_pattern, x, re.UNICODE)


def default_tokenizer(x):
    """Make tokens of a file path or string.

    :param x: The filepath of string.
    :type x: WindowsFilePath, PosixFilePath, str

    :return: list of tokens (strings)
    :return_type: list
    """
    return tokenizer(x, DEFAULT_TOKENIZE_PATTERN)


def path_tokenizer(x):
    """Make parts of a file path.

    :param x: The filepath .
    :type x: WindowsFilePath, PosixFilePath, str

    :return: list of path parts (strings)
    :return_type: list
    """
    return tokenizer(x, DEFAULT_PATH_SPLIT_PATTERN)


def camel_splitter(x):
    """Make tokens from camelCase strings

    :param x: The filepath of string.
    :type x: WindowsFilePath, PosixFilePath, str

    :return: list of tokens (strings)
    :return_type: list
    """

    raise NotImplementedError


def title_splitter(x):
    """Make tokens from title formatted strings

    :param x: The filepath of string.
    :type x: WindowsFilePath, PosixFilePath, str

    :return: list of tokens (strings)
    :return_type: list
    """

    raise NotImplementedError
