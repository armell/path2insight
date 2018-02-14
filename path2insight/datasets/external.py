import os

from path2insight.parse import parse_from_pandas


def load_pride(nrows=None, skiprows=None):
    """Load the filepaths of the PRIDE proteomics archive.

    "The PRIDE PRoteomics IDEntifications (PRIDE) database is a
    centralized, standards compliant, public data repository for
    proteomics data, including protein and peptide identifications,
    post-translational modifications and supporting spectral
    evidence. PRIDE is a core member in the ProteomeXchange (PX)
    consortium, which provides a single point for submitting mass
    spectrometry based proteomics data to public-domain repositories.
    Datasets are submitted to PRIDE via ProteomeXchange and are
    handled by expert biocurators.
    (https://www.ebi.ac.uk/pride/archive/)"

    The filepaths from of this dataset are loaded with this function.
    The data can be found at
    ftp://ftp.pride.ebi.ac.uk/pride/data/archive/. The snapshot was
    taken on 06 february 2018 with a Linux device with the
    ftp://ftp.pride.ebi.ac.uk/pride/data/archive/ as a mounted drive.

    :param nrows: Number of rows of file to read. Useful for reading
        pieces of large files
    :type nrwos: int

    :param skiprows: Line numbers to skip (0-indexed) or number of
        lines to skip (int) at the start of the file. See
        pandas.read_csv() for more information about this parameter.
    :type skiprows: list-like or integer or callable, default None

    :return: A list of PosixFilePaths of the PRIDE dataset.
    :return_type: list

    """

    try:
        import pandas as pd
    except ImportError:
        raise ImportError('pandas is required for this function')

    data_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'pride.csv.gzip'
    )

    data = pd.read_csv(data_path, nrows=nrows, skiprows=skiprows,
                       encoding='utf-8', compression='gzip')

    return parse_from_pandas(data, os_name='posix')


def load_ensembl(nrows=None, skiprows=None):
    """Load the filepaths of the Ensembl dataset (release 90).

    "Ensembl is a genome browser for vertebrate genomes that supports
    research in comparative genomics, evolution, sequence variation
    and transcriptional regulation. Ensembl annotate genes, computes
    multiple alignments, predicts regulatory function and collects
    disease data. Ensembl tools include BLAST, BLAT, BioMart and the
    Variant Effect Predictor (VEP) for all supported species.
    (ensembl.org)"

    The filepaths from release-90 of this dataset are loaded with this
    function. The data can be found at
    ftp://ftp.ensembl.org/pub/release-90/. The snapshot was taken on
    16 November 2017 with a Linux device with the
    ftp://ftp.ensembl.org/pub/release-90/ as a mounted drive.


    :param nrows: Number of rows of file to read. Useful for reading
        pieces of large files
    :type nrwos: int

    :param skiprows: Line numbers to skip (0-indexed) or number of
        lines to skip (int) at the start of the file. See
        pandas.read_csv() for more information about this parameter.
    :type skiprows: list-like or integer or callable, default None

    :return: A list of PosixFilePaths of the PRIDE dataset.
    :return_type: list

    """

    try:
        import pandas as pd
    except ImportError:
        raise ImportError('pandas is required for this function')

    data_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'ensembl90.csv.gzip'
    )

    data = pd.read_csv(data_path, nrows=nrows, skiprows=skiprows,
                       encoding='ascii', compression='gzip')

    return parse_from_pandas(data, os_name='posix')
