import pytest

from websharecli import commands


@pytest.mark.parametrize("query, expected", [
    ('', ''),
    ('a', 'a'),
    ('a ', 'a'),
    ('A', 'a'),
    ('a b B', 'a b'),
    ('a b c B', 'a b c'),
])
def test_normalize_query(query, expected):
    assert commands.normalize_query(query) == expected


@pytest.mark.parametrize("query, options, expected", [
    ('a', None, ['a']),
    ('a', [], ['a']),
    ('a', [''], ['a']),
    ('a', ['a'], ['a']),
    ('A', ['a'], ['a']),
    ('a', ['x'], ['a x']),
    ('a', ['x a'], ['a x']),
    ('a', ['x y'], ['a x y']),
    ('a', ['x', 'y'], ['a x', 'a y']),
    ('a b', ['x'], ['a b x']),
    ('a bc', ['a', 'c'], ['a bc', 'a bc c']),
])
def test_query_expand(query, options, expected):
    assert commands.query_expand(query, options) == expected


def test_query_complete_wildcard():
    query = 'test *'
    results = ['test {:02d}'.format(i) for i in range(100)]
    assert commands.query_complete_wildcard(query) == results
    query = 'test'
    results = ['test']
    assert commands.query_complete_wildcard(query) == results
