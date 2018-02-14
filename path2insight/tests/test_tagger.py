import re

import path2insight

from path2insight.explore import FolderTagger, TypeTagger, TokenTypeTagger


def test_folder_tagger():

    data = [
        path2insight.WindowsFilePath('D:/data/armel/'),
        path2insight.WindowsFilePath('D:/data/armel/file1.xyz'),
        path2insight.WindowsFilePath('D:/data/armel/file2.xyz'),
        path2insight.WindowsFilePath('D:/data/armel/file3.xyz'),
        path2insight.WindowsFilePath('D:/data/armel/file4.xyz'),
    ]
    expected = [
        (path2insight.WindowsFilePath('D:/data/armel/'), 'FOLDER'),
        (path2insight.WindowsFilePath('D:/data/armel/file1.xyz'), 'FILE'),
        (path2insight.WindowsFilePath('D:/data/armel/file2.xyz'), 'FILE'),
        (path2insight.WindowsFilePath('D:/data/armel/file3.xyz'), 'FILE'),
        (path2insight.WindowsFilePath('D:/data/armel/file4.xyz'), 'FILE'),
    ]

    tagger = FolderTagger()
    result = tagger.tag(data)

    assert result == expected


def test_type_tagger():

    data = [
        path2insight.WindowsFilePath('D:/data/armel/'),
        path2insight.WindowsFilePath('D:/data/armel_jonathan/file1.xyz'),
        path2insight.WindowsFilePath('D:/data/armel/file2.xyz'),
        path2insight.WindowsFilePath('D:/data/armel_jonathan/file3 test.xyz'),
        path2insight.WindowsFilePath('D:/data/armel/file4.xyz'),
    ]
    expected = [
        [('D:\\', 'DRV'), ('data', 'FLD'), ('armel', 'FLD')],
        [('D:\\', 'DRV'), ('data', 'FLD'), ('armel_jonathan', 'FLD'),
         ('file1', 'STM'), ('.xyz', 'EXT')],
        [('D:\\', 'DRV'), ('data', 'FLD'), ('armel', 'FLD'),
         ('file2', 'STM'), ('.xyz', 'EXT')],
        [('D:\\', 'DRV'), ('data', 'FLD'), ('armel_jonathan', 'FLD'),
         ('file3 test', 'STM'), ('.xyz', 'EXT')],
        [('D:\\', 'DRV'), ('data', 'FLD'), ('armel', 'FLD'),
         ('file4', 'STM'), ('.xyz', 'EXT')]]

    tagger = TypeTagger()
    result = tagger.tag(data)
    assert result == expected


def test_token_type_tagger():

    data = [
        path2insight.WindowsFilePath('D:/data/armel/'),
        path2insight.WindowsFilePath('D:/data/armel_jonathan/file1.xyz'),
        path2insight.WindowsFilePath('D:/data/armel/file2.xyz'),
        path2insight.WindowsFilePath('D:/data/armel_jonathan/file3 test.xyz'),
        path2insight.WindowsFilePath('D:/data/armel/file4.xyz'),
    ]
    expected = [
        [('D:', 'DRV'), ('data', 'FLD'), ('armel', 'FLD')],
        [('D:', 'DRV'), ('data', 'FLD'), ('armel', 'FLD'),
         ('jonathan', 'FLD'), ('file1', 'STM'), ('.xyz', 'EXT')],
        [('D:', 'DRV'), ('data', 'FLD'), ('armel', 'FLD'),
         ('file2', 'STM'), ('.xyz', 'EXT')],
        [('D:', 'DRV'), ('data', 'FLD'), ('armel', 'FLD'),
         ('jonathan', 'FLD'), ('file3', 'STM'), ('test', 'STM'),
         ('.xyz', 'EXT')],
        [('D:', 'DRV'), ('data', 'FLD'), ('armel', 'FLD'),
         ('file4', 'STM'), ('.xyz', 'EXT')]]

    tagger = TokenTypeTagger()
    result = tagger.tag(data)
    assert result == expected

    expected = [
        [('D:\\', 'DRV'), ('data', 'FLD'), ('armel', 'FLD')],
        [('D:\\', 'DRV'), ('data', 'FLD'), ('armel_jonathan', 'FLD'),
         ('file1', 'STM'), ('.xyz', 'EXT')],
        [('D:\\', 'DRV'), ('data', 'FLD'), ('armel', 'FLD'),
         ('file2', 'STM'), ('.xyz', 'EXT')],
        [('D:\\', 'DRV'), ('data', 'FLD'), ('armel_jonathan', 'FLD'),
         ('file3', 'STM'), ('test', 'STM'), ('.xyz', 'EXT')],
        [('D:\\', 'DRV'), ('data', 'FLD'), ('armel', 'FLD'),
         ('file4', 'STM'), ('.xyz', 'EXT')]]

    def custom_tokenizer(x):
        return re.split(r"\s+", x)

    tagger = TokenTypeTagger(tokenizer=custom_tokenizer)
    result = tagger.tag(data)
    assert result == expected


def test_extension_document_tagger():

    data = [
        path2insight.WindowsFilePath('D:/data/armel/README'),
        path2insight.WindowsFilePath('D:/data/armel/file1.doc'),
        path2insight.WindowsFilePath('D:/data/armel/file2.docx'),
        path2insight.WindowsFilePath('D:/data/armel/file3.pptx'),
        path2insight.WindowsFilePath('D:/data/armel/file4.raw'),
    ]
    expected = ['', 'DOCUMENT', 'DOCUMENT', 'PRESENTATION', '']

    tagger = path2insight.DocumentTagger()
    result = tagger.tag(data)

    assert result == expected


def test_extension_compression_tagger():

    data = [
        path2insight.WindowsFilePath('D:/data/armel/README'),
        path2insight.WindowsFilePath('D:/data/armel/file1.zip'),
        path2insight.WindowsFilePath('D:/data/armel/file2.gz'),
        path2insight.WindowsFilePath('D:/data/armel/file3.tar'),
        path2insight.WindowsFilePath('D:/data/armel/file4.bz2'),
    ]
    expected = ['', 'ARCHIVE_AND_COMPRESSION', 'ARCHIVE_AND_COMPRESSION',
                'ARCHIVE', 'COMPRESSION']

    tagger = path2insight.CompressionTagger()
    result = tagger.tag(data)

    assert result == expected
