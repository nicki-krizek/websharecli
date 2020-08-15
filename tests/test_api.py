import os
import pytest
import requests_mock

from websharecli import api


def mock_query(command, data_file):
    """Mock POST requests against endpoint with static data"""
    def wrap(func):
        def wrapped_f(*args, **kwargs):
            file_path = os.path.join('tests', 'mock', command, data_file)
            file_path += '.xml'
            with requests_mock.Mocker() as mock:
                with open(file_path, 'r') as file_:
                    mock.post(api.ENDPOINTS[command], text=file_.read())
                    func(*args, **kwargs)
        return wrapped_f
    return wrap


@mock_query('search', 'no_result')
def test_search_no_result():
    files = api.search('')
    assert len(files) == 0


@mock_query('search', 'ok')
def test_search_ok():
    files = api.search('linux iso', limit=2)
    assert len(files) == 2
    assert files[0]['ident'] == '5Vw5vv6H47'
    assert files[0]['name'] == '2mini linux.iso'
    assert files[0]['type'] == 'iso'
    assert int(files[0]['size']) == 111149056
    assert int(files[0]['positive_votes']) == 0
    assert int(files[0]['negative_votes']) == 0
    assert files[1]['ident'] == 'xsxy0Io3Qg'


@mock_query('search', 'fatal')
def test_search_fatal():
    with pytest.raises(Exception):
        api.search('')


@mock_query('file_link', 'ok')
def test_file_link_ok():
    link = api.file_link('xsxy0Io3Qg')
    assert link == (
        "http://vip.3.dl.webshare.cz/0029/xsxy0Io3Qg/300000/eyJhZGRyIjoiODku"
        "MTAyLjMxLjE5IiwidmFsaWRfdG8iOjE1MDkyNzY3NzcsInVzZXJfaWQiOm51bGwsImZy"
        "ZWUiOjF9/a85a2ad2a4ca592b9d9a70ce634c6874/Linux-Ubuntu-12.10---"
        "Quantal-Quetzal-x64.iso")


@mock_query('file_link', 'not_found')
def test_file_link_not_found():
    with pytest.raises(api.LinkUnavailableException):
        api.file_link('xxxxxxxxx')


def test_api_compat_search():
    data = {'what': 'test', 'sort': 'largest', 'limit': '2'}
    resp = api.query(api.ENDPOINTS['search'], data)
    assert resp['status'] == 'OK'
    assert 'file' in resp
    assert 'total' in resp
    entry = resp['file'][0]
    assert 'ident' in entry
    assert 'name' in entry
    assert 'type' in entry
    assert 'size' in entry
    assert 'positive_votes' in entry
    assert 'negative_votes' in entry


def test_api_compat_file_link():
    data = {'ident': '79J2zP3h03'}
    resp = api.query(api.ENDPOINTS['file_link'], data)
    assert resp['status'] == 'OK'
    assert 'link' in resp
