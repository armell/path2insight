from __future__ import division

import time
import os

from path2insight.core import WindowsFilePath, PosixFilePath


def walk(d, delay=None, **kwargs):
    """Walk the file system like os.walk.

    Function to collect file paths from the file system. This function
    is useful for collecting and sharing the file paths. The function
    is similar to os.walk.

    :param d: The path to the directory.
    :type d: str
    :param delay: Time delay between requesting paths.
    :type delay: (list of) str
    :param kwargs: Additional kwargs for os.walk.

    :return: Return the file paths and folder paths. The function
        returns a tuples with (files, folders)
    :return_type: (list, list)

    :Example:

    Collect and share filepaths with pandas.

    >>> import pandas as pd
    >>> import path2insight
    >>> files, folders = path2insight.walk('.')
    >>> pd.DataFrame(files).to_csv("export_filepaths.csv", index=False)

    """

    if os.name == 'nt':
        FilePath = WindowsFilePath
    else:
        FilePath = PosixFilePath

    walk_gen = os.walk(d, **kwargs)

    files = []
    folders = []

    while True:

        try:
            root, fld, fls = next(walk_gen)

            # iter files
            for f in fls:
                files.append(FilePath(root, f))

            # iter folders
            for folder in fld:
                folders.append(FilePath(root, folder))

            if delay:
                time.sleep(delay / 1000)

        except StopIteration:
            break

    return files, folders
