"""String distance algorithms."""

from path2insight.utils import _import_jellyfish


def levenshtein(list1_str, list2_str=None):
    """Internal function to compute the Levenshtein distance."""

    lv = _import_jellyfish()

    if list2_str is None:
        list2_str = list1_str

    return [[lv(s1, s2) for s2 in list2_str] for s1 in list1_str]


def levenshtein_normalised(list1_str, list2_str=None):
    """Internal function to compute the Levenshtein distance."""

    lv = _import_jellyfish()

    if list2_str is None:
        list2_str = list1_str

    return [[lv(s1, s2) / max(len(s1), len(s2)) for s2 in list2_str]
            for s1 in list1_str]
