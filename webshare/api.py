import requests
from urllib.parse import urljoin
import xmltodict


API_URI = 'https://webshare.cz/api/'
ENDPOINTS = {
    'search': urljoin(API_URI, 'search/'),
    'file_link': urljoin(API_URI, 'file_link/')}


def query(url, data):
    # TODO add wst to data
    req = requests.post(url, data=data)
    resp = xmltodict.parse(req.text)['response']
    if resp['status'] != 'OK':
        raise Exception(
            "api error: returned status: {}".format(resp['status']))
    return resp


def search(what, sort='', limit=10):
    # force min limit to 2 -- avoid special case handling of single result
    limit = str(limit) if int(limit) != 1 else '2'
    data = {
        'what': what,
        'sort': sort,
        'limit': limit}
    resp = query(ENDPOINTS['search'], data)
    total = int(resp['total'])
    if total == 0:
        return []
    return resp['file']


def file_link(ident):
    data = {'ident': ident}
    try:
        resp = query(ENDPOINTS['file_link'], data)
    except Exception:
        return None
    return resp['link']
