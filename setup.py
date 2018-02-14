"""Setup script for path2insight"""

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def get_version_number():
    """Get the version number."""

    try:
        here = path.abspath(path.dirname(__file__))
        init = path.join(here, 'path2insight', '__init__.py')

        # Get the long description from the README file
        with open(init, encoding='utf-8') as f:
            for line in f.readlines():
                if line.startswith('__version__'):
                    return line.split("\"")[1]
                    break
    except Exception:
        pass

    return "unknown"


REQUIRED_DEPENDENCIES = []

# check if pathlib is available. If not, install pathlib2 (from pypi)
try:
    import pathlib
except ImportError:
    REQUIRED_DEPENDENCIES.append('pathlib2')

setup(
    name='path2insight',

    version=get_version_number(),

    description='A set of tools to retrieve information from filepaths.',
    long_description=long_description,

    url='https://github.com/armell/path2insight',

    author='Armel Lefebvre, Jonathan de Bruin',
    author_email='A.E.J.Lefebvre@uu.nl, j.debruin1@uu.nl',

    license='MIT',

    classifiers=[

        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='filepath pathlib datamanagement exploration',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=REQUIRED_DEPENDENCIES,
    extras_require={
        'test': ['pytest', 'parameterized'],
    },
    package_data={
        '': ['datasets/data/ensembl90.csv.gzip',
             'datasets/data/pride.csv.gzip'],
    }
)