from collections import Counter

from path2insight.explore import token_counts
from path2insight.utils import MissingDependencyError


def distance_on_token(x, y=None, tokenizer=None, metric='l2', n_jobs=1):
    """Compute the distance between filenames based on tokens.

    The distance between filenames is computed based on the number of tokens
    that both filenames have in common.

    :param x: A list of filepath objects
    :type x: list
    :param y: A list of filepath pbjects to compare x with. If y is None, the
        internal similarity of the filepaths in x are computed.
    :type y: list
    :param tokenizer: Not implemented yet.
    :type tokenizer: callable
    :param metric: The distance metric like 'cityblock', 'cosine', 'euclidean',
        'l1', 'l2', 'manhattan'. See http://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.pairwise_distances.html
        for all possible metrics. Default 'l2'.
    :type metric: string, or callable
    :param n_jobs: The number of cores to use during the computation of the
        metric. Default 1.
    :type n_jobs: int

    :Example:

    >>> from path2insight.explore import distance_on_token
    >>> import seaborn as sns

    >>> d = distance_on_token(DATASET)
    >>> sns.heatmap(d)

    :Note:

    For visual inspection, the `heatmap` function in seaborn can be useful.

    """

    try:
        from sklearn.metrics import pairwise_distances
        from sklearn.feature_extraction import DictVectorizer
    except ModuleNotFoundError:
        raise MissingDependencyError(
            "Install the module 'sklearn' to compute distances.")

    dict_x = [dict(token_counts([path], lower=True)) for path in x]
    if y:
        dict_y = [dict(token_counts([path], lower=True)) for path in y]

    dict_input = dict_x if y is None else dict_x + dict_y

    dv = DictVectorizer().fit(dict_input)
    matrix_x_sparse = dv.transform(dict_x)
    if y:
        matrix_y_sparse = dv.transform(dict_y)
    else:
        matrix_y_sparse = matrix_x_sparse

    return pairwise_distances(matrix_x_sparse, matrix_y_sparse,
                              metric=metric, n_jobs=n_jobs)


def distance_on_extension(x, y=None, tokenizer=None, metric='l2', n_jobs=1):
    """Compute the distance between filenames based on the extension.

    The distance between filenames is computed based on the number of
    extensions that both filenames have in common.

    :param x: A list of filepath objects
    :type x: list
    :param y: A list of filepath pbjects to compare x with. If y is None, the
        internal similarity of the filepaths in x are computed.
    :type y: list
    :param metric: The distance metric like 'cityblock', 'cosine', 'euclidean',
        'l1', 'l2', 'manhattan'. See http://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.pairwise_distances.html
        for all possible metrics. Default 'l2'.
    :type metric: string, or callable
    :param n_jobs: The number of cores to use during the computation of the
        metric. Default 1.
    :type n_jobs: int

    :Example:

    >>> from path2insight.explore import distance_on_extension
    >>> import seaborn as sns

    >>> d = distance_on_extension(DATASET)
    >>> sns.heatmap(d)

    :Note:

    For visual inspection, the `heatmap` function in seaborn can be useful.

    """

    try:
        from sklearn.metrics import pairwise_distances
        from sklearn.feature_extraction import DictVectorizer
    except ModuleNotFoundError:
        raise MissingDependencyError(
            "Install the module 'sklearn' to compute distances.")

    dict_x = [dict(Counter(path.suffixes)) for path in x]
    if y:
        dict_y = [dict(Counter(path.suffixes)) for path in y]

    dict_input = dict_x if y is None else dict_x + dict_y

    dv = DictVectorizer().fit(dict_input)
    matrix_x_sparse = dv.transform(dict_x)
    if y:
        matrix_y_sparse = dv.transform(dict_y)
    else:
        matrix_y_sparse = matrix_x_sparse

    return pairwise_distances(matrix_x_sparse, matrix_y_sparse, metric=metric)


def distance_on_depth(x, y=None, metric='l2', n_jobs=1):
    """Compute the distance between filenames based on the depth.

    The distance between filenames is computed based on the difference
    in depth between the filenames.

    :param x: A list of filepath objects
    :type x: list
    :param y: A list of filepath pbjects to compare x with. If y is None, the
        internal similarity of the filepaths in x are computed.
    :type y: list
    :param metric: The distance metric like 'cityblock', 'cosine', 'euclidean',
        'l1', 'l2', 'manhattan'. See http://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.pairwise_distances.html
        for all possible metrics. Default 'l2'.
    :type metric: string, or callable
    :param n_jobs: The number of cores to use during the computation of the
        metric. Default 1.
    :type n_jobs: int

    :Example:

    >>> from path2insight.explore import distance_on_depth
    >>> import seaborn as sns

    >>> d = distance_on_depth(DATASET)
    >>> sns.heatmap(d)

    :Note:

    For visual inspection, the `heatmap` function in seaborn can be useful.

    """

    try:
        from sklearn.metrics import pairwise_distances
        import numpy
    except ModuleNotFoundError:
        raise MissingDependencyError(
            "Install the module 'sklearn' to compute distances.")

    arr_x = numpy.array([len(path.parts) for path in x], ndmin=2).T
    if y:
        arr_y = numpy.array([len(path.parts) for path in y], ndmin=2).T
    else:
        arr_y = arr_x

    return pairwise_distances(arr_x, arr_y, metric=metric)
