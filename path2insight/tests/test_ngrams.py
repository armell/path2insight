import path2insight


def test_bigrams():

    data = ["first", "second", "third", "fourth"]

    expected = [('first', 'second'), ('second', 'third'), ('third', 'fourth')]

    result = list(path2insight.ngrams(data, 2))
    assert result == expected

    result = list(path2insight.bigrams(data))
    assert result == expected


def test_trigrams():

    data = ["first", "second", "third", "fourth"]

    expected = [('first', 'second', 'third'), ('second', 'third', 'fourth')]

    result = list(path2insight.ngrams(data, 3))
    assert result == expected

    result = list(path2insight.trigrams(data))
    assert result == expected


def test_padding():

    data = ["first", "second", "third", "fourth"]

    expected = [(None, 'first'),
                ('first', 'second'),
                ('second', 'third'),
                ('third', 'fourth'),
                ('fourth', None)]

    result = list(path2insight.ngrams(data, 2, pad_left=True, pad_right=True))
    assert result == expected

    result = list(path2insight.bigrams(data, pad_left=True, pad_right=True))
    assert result == expected
