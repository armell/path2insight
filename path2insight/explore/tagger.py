"""
This module implements a filepath tagger. The object structure of this
filepath tagger is based on the tagger objects in the Natural Language
Toolkit (NLTK).
"""

import fnmatch
from collections import OrderedDict, Counter

from path2insight.decorators import iter_advanced_method
from path2insight.tokenizers import default_tokenizer
from path2insight.utils import (string_and_binary_types,
                                unique,
                                iteritems)


class Tagger(object):
    """Base class for the taggers."""


class FolderTagger(Tagger):
    """
    [EXPERIMENTAL] A tagger that assigns a FOLDER or FILE tag to each path.

        >>> from path2insight.explore import FolderTagger
        >>> folder_tagger = FolderTagger()
        >>> list(folder_tagger.tag([WindowsFilePath('D:/armel/file.xyz')])
        [(WindowsFilePath('D:/armel/file.xyz'), 'FILE')]
    """

    def __init__(self):
        pass

    @iter_advanced_method
    def tag(self, x):

        return [(fp, "FILE" if fp.suffix else "FOLDER") for fp in x]


class BaseTypeTagger(Tagger):
    """
    The base class for the type taggers.

    :param tokenizer: A tokenizer function to split the filepath parts.
    :type tokenizer: list
    :param tag_names: The names of the four tags that this tagger uses.
        The tags default tags are drive="DRV", folder="FLD", stem="STM"
        and extension="EXT".
    :type tag_names: list

    """

    def __init__(self, tokenizer=None, tag_names=None):

        self.tokenizer = tokenizer

        # drive, folder, stem, extension
        if tag_names:

            if len(tag_names) != 4:
                raise ValueError('The list has an incorrrect length, '
                                 'expected a length of 4.')
            self.tag_names = tag_names
        else:
            self.tag_names = ["DRV", "FLD", "STM", "EXT"]

    def _part_tokenizer(self, part, tag):

        if callable(self.tokenizer):
            return [(token, tag) for token in self.tokenizer(part)]
        else:
            return [(part, tag)]

    @iter_advanced_method
    def tag(self, x):
        """
        Return a list with the parts/tokens and their tags.

        :param x: A list with WindowsFilePath and PosixFilePath objects.
        :type x: list

        :return: A list of lists for which each nested list is a 2-tuple of
            name and tag.
        :return_type: list

        """

        result = []

        for fp in x:

            tagged_path = []

            parts = fp.parts
            part_i = 0

            if len(parts) == 0:
                continue

            # check drive
            if parts[part_i] == (fp.drive + fp.root):
                tagged_tokens = self._part_tokenizer(
                    parts[0], self.tag_names[0])
                tagged_path = tagged_path + tagged_tokens
                part_i = part_i + 1

            for part in parts[part_i:-1]:
                tagged_tokens = self._part_tokenizer(part, self.tag_names[1])
                tagged_path = tagged_path + tagged_tokens
                part_i = part_i + 1

            # based on pathlib.py
            name = parts[-1]
            i = name.rfind('.')
            if 0 < i < len(name) - 1:
                tagged_tokens = self._part_tokenizer(
                    name[:i], self.tag_names[2])
                tagged_path = tagged_path + tagged_tokens
                # ext is not tokenized
                tagged_path.append((name[i:], self.tag_names[3]))
            else:
                tagged_tokens = self._part_tokenizer(name, self.tag_names[1])
                tagged_path = tagged_path + tagged_tokens

            result.append(tagged_path)

        return result


class TypeTagger(BaseTypeTagger):
    """
    A tagger that tags each filepath part (and extension) with the following
    labels: drive (DRV), folder (FLD), stem (STEM) and extension (EXT).

    :param tag_names: The names of the four tags that this tagger uses.
        The tags default tags are drive="DRV", folder="FLD", stem="STM"
        and extension="EXT".
    :type tag_names: list
    """

    def __init__(self, tag_names=None):
        super(TypeTagger, self).__init__(tokenizer=None, tag_names=tag_names)


class TokenTypeTagger(BaseTypeTagger):
    """
    A tagger that tags each filepath part (and extension) with the following
    labels: drive (DRV), folder (FLD), stem (STEM) and extension (EXT).

    :param tokenizer: A function that converts a filepath or string into
        tokens.
    :type tokenizer: callable
    :param tag_names: The names of the four tags that this tagger uses.
        The tags default tags are drive="DRV", folder="FLD", stem="STM"
        and extension="EXT".
    :type tag_names: list
    """

    def __init__(self, tokenizer=default_tokenizer, tag_names=None):
        super(TokenTypeTagger, self).__init__(
            tokenizer=tokenizer, tag_names=tag_names)


class ExtensionTagger(object):
    """Extension tagger based on dict of tags.

    Unix shell-style wildcards like * and ? are supported.

    :param tags: A dict with the extensions to tag. The keys of the dict are
        the tags and the values of the dict are lists with extensions.
    :type tags: dict
    :param na_tag: The tag for an extension that is not in the tags
        dictonairy. Default ''.
    :type na_tag: str, None, object
    :ignore_case: bool
        Case-insensitive extension tagging. Default False.
    :use_wildcards: bool
        Use Unix shell-style wildcards like * and ?. Default True.

    Note:

    Use an OrderedDict in case of order prevelence.

    """

    def __init__(self, tags={}, na_tag='', ignore_case=False,
                 use_wildcards=True):

        self.tags = tags
        self.na_tag = na_tag
        self.ignore_case = ignore_case
        self.use_wildcards = use_wildcards

    def _tags(self):
        """Inverts tags.

        Input:
        {"DOC", [".doc*", ".txt"]}
        Returns:
        [(".doc*", "DOC"), (".txt", "DOC")]
        """
        _tags = self.tags

        tags = []
        for tag, pattern in iteritems(_tags):
            if isinstance(pattern, string_and_binary_types):
                pattern_list = [pattern]
            else:
                pattern_list = pattern

            for pat in pattern_list:
                tags.append((pat, tag))

        # convert to lower when we are ignoring the case
        if self.ignore_case:
            tags = [(pattern.lower(), tag) for pattern, tag in tags]

        return tags

    def _get_extensions(self, x):

        if self.ignore_case:
            return [path.extension.lower() for path in x]
        else:
            return [path.extension for path in x]

    def _validate_mapping(self, mapping):

        patterns = [pattern for pattern, tag in mapping]
        if len(patterns) > len(unique(patterns)):
            dups = [item for item, count in Counter(patterns).items()
                    if count > 1]
            raise ValueError("Multiple tags pointing to the "
                             "same extension {!r}.".format(dups))

    def _transform_wildcards(self, mapping, x):

        # check which extenions (in the tags list) do have a wildcard
        unique_extensions = None
        mapping_wo_wildcards = []

        for pattern, tag in mapping:

            # if a linux wildcard is found
            if "*" in pattern or "?" in pattern:

                # initialise a set of unique extensions if not exist
                if unique_extensions is None:
                    unique_extensions = unique([ext for ext in x])

                # Add a list with all matching patterns for this pattern
                for pat_match in fnmatch.filter(unique_extensions, pattern):
                    mapping_wo_wildcards.append((pat_match, tag))
            else:
                mapping_wo_wildcards.append((pattern, tag))

        return mapping_wo_wildcards

    @iter_advanced_method
    def tag(self, x):
        """Return a list with the extension tag for each file path.

        :param x: A list with WindowsFilePath and PosixFilePath objects.
        :type x: list

        :return: A list with the tag(s) for each filepath.
        :return_type: list
        """

        x_extensions = self._get_extensions(x)

        mapping = self._tags()
        if self.use_wildcards:
            mapping = self._transform_wildcards(mapping, x_extensions)

        self._validate_mapping(mapping)

        mapping_dict = OrderedDict(mapping)

        result = []
        for ext in x_extensions:
            try:
                result.append(mapping_dict[ext])
            except KeyError:
                result.append(self.na_tag)

        return result


class CompressionTagger(ExtensionTagger):
    """CompressionTagger(tags=..., na_tag='', ignore_case=True, use_wildcards=True)

    Extension tagger for compression and archiving.

    This tagger tags compressed file paths based on their extension. There are
    three different types of tags in this tagger. The tags are:

    - ARCHIVE
    - COMPRESSION
    - ARCHIVE_AND_COMPRESSION

    :param tags: A dict with the extensions to tag. The keys of the dict are
        the tags and the values of the dict are lists with extensions.
    :type tags: dict
    :param na_tag: The tag for an extension that is not in the tags
        dictonairy. Default ''.
    :type na_tag: str, None, object
    :ignore_case: bool
        Case-insensitive extension tagging. Default False.
    :use_wildcards: bool
        Use Unix shell-style wildcards like * and ?. Default True.
    """

    # import lists with datasets
    from path2insight.datasets.extensions import (
        EXTENSIONS_ARCHIVE,
        EXTENSIONS_COMPRESSION,
        EXTENSIONS_ARCHIVE_AND_COMPRESSION
    )

    tags = {
        'COMPRESSION': EXTENSIONS_COMPRESSION,
        'ARCHIVE': EXTENSIONS_ARCHIVE,
        'ARCHIVE_AND_COMPRESSION': EXTENSIONS_ARCHIVE_AND_COMPRESSION
    }

    def __init__(self, tags=tags, *args, **kwargs):
        super(CompressionTagger, self).__init__(tags=tags, *args, **kwargs)


class DocumentTagger(ExtensionTagger):
    """DocumentTagger(tags=..., na_tag='', ignore_case=True, use_wildcards=True)

    Extension tagger for documents.

    This tagger tags compressed file paths based on their extension. There are
    three different types of tags in this tagger. The tags are:

    - DOCUMENT
    - PRESENTATION

    :param tags: A dict with the extensions to tag. The keys of the dict are
        the tags and the values of the dict are lists with extensions.
    :type tags: dict
    :param na_tag: The tag for an extension that is not in the tags
        dictonairy. Default ''.
    :type na_tag: str, None, object
    :ignore_case: bool
        Case-insensitive extension tagging. Default False.
    :use_wildcards: bool
        Use Unix shell-style wildcards like * and ?. Default True.
    """

    # import lists with datasets
    from path2insight.datasets.extensions import (
        EXTENSIONS_DOCUMENT,
        EXTENSIONS_PRESENTATION,
        EXTENSIONS_IMAGE
    )

    tags = {
        'DOCUMENT': EXTENSIONS_DOCUMENT,
        'PRESENTATION': EXTENSIONS_PRESENTATION,
        'IMAGE': EXTENSIONS_IMAGE
    }

    def __init__(self, tags=tags, *args, **kwargs):
        super(DocumentTagger, self).__init__(tags=tags, *args, **kwargs)
