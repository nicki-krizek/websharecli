from webshare.data import File


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
