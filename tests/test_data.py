import pytest

from websharecli.data import File, filter_unique, filter_extensions, filter_exclude


TEST_API_FILE = {
    'ident': '5Vw5vv6H47',
    'name': '2mini linux.iso',
    'type': 'iso',
    'size': '111149056',
    'positive_votes': 3,
    'negative_votes': '1',
}


def test_file_object():
    file_ = File(**TEST_API_FILE)
    assert file_.ident == '5Vw5vv6H47'
    assert file_.name == '2mini linux.iso'
    assert file_.type == 'iso'
    assert file_.size == 111149056
    assert file_.rating == 2


@pytest.mark.parametrize('name, query, matches', [
    ('a', 'a', True),
    ('A', 'a', True),
    ('b', 'a', False),
    ('a b', 'A', True),
    ('b a', 'a', True),
    ('a b c', 'c a', True),
    ('a.b', 'a', True),
    ('abc', 'a', True),
    ('a-b.c', 'a-b b', True),
    ('a.b.c', 'ab', False),
])
def test_file_matches_query(name, query, matches):
    file_ = File(name=name)
    assert file_.matches_query(query) == matches


@pytest.mark.parametrize('idents, uniques', [
    (['1'], ['1']),
    (['1', '1'], ['1']),
    (['1', '2'], ['1', '2']),
    (['1', '2', '1', '3', '3', '1'], ['1', '2', '3']),
])
def test_filter_unique(idents, uniques):
    filtered = filter_unique([File(ident=ident) for ident in idents])
    uniques = [File(ident=ident) for ident in uniques]
    assert all([f1 == f2 for f1, f2 in zip(filtered, uniques)])


def test_filter_extensions():
    files_ = [
        File(ident='1', type='a'),
        File(ident='2', type='b'),
        File(ident='3', type='c'),
        File(ident='4', type='a'),
        File(ident='5', type='ab'),
    ]
    assert filter_extensions(files_, None) == files_
    assert len(filter_extensions(files_, [])) == 0
    filtered = filter_extensions(files_, ['a', 'b'])
    assert len(filtered) == 3
    assert files_[0] in filtered
    assert files_[1] in filtered
    assert files_[3] in filtered


def test_filter_exclude():
    files_ = [
        File(name='x'),
        File(name='720p'),
        File(name='hdr.720p'),
        File(name='hdr'),
        File(name='HDR'),
        File(name='hDR'),
        File(name='ahdr'),
        File(name='ahdrb'),
        File(name='a.hdr'),
    ]
    assert filter_exclude(files_, None) == files_
    assert filter_exclude(files_, []) == files_

    filtered = filter_exclude(files_, 'hdr')
    assert len(filtered) == 2
    assert files_[0] in filtered
    assert files_[1] in filtered

    filtered = filter_exclude(files_, 'HDR')
    assert len(filtered) == 2
    assert files_[0] in filtered
    assert files_[1] in filtered

    filtered = filter_exclude(files_, ['HdR', '720'])
    assert len(filtered) == 1
    assert files_[0] in filtered
