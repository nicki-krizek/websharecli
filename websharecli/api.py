import requests
from urllib.parse import urljoin
import xmltodict

from websharecli.config import CONFIG


API_URI = 'https://webshare.cz/api/'
ENDPOINTS = {
    'search': urljoin(API_URI, 'search/'),
    'file_link': urljoin(API_URI, 'file_link/')}


class LinkUnavailableException(Exception):
    pass


def query(url, data):
    req = requests.post(url, data=data)
    resp = xmltodict.parse(req.text)['response']
    if resp['status'] != 'OK':
        raise Exception(
            "api error: returned status: {}".format(resp['status']))
    return resp


def search(what, sort='largest', limit=5):
    # force min limit to 2 -- avoid special case handling of single result
    limit = str(limit) if int(limit) != 1 else '2'
    data = {
        'what': what,
        'sort': sort,
        'limit': limit,
        'wst': CONFIG.wst,
    }
    resp = query(ENDPOINTS['search'], data)
    total = int(resp['total'])
    if total == 0:
        return []
    elif total == 1:
        return [resp['file']]
    return resp['file']


def file_link(ident):
    data = {'ident': ident, 'wst': CONFIG.wst}
    try:
        resp = query(ENDPOINTS['file_link'], data)
    except Exception as exc:
        raise LinkUnavailableException from exc
    if CONFIG.force_vip and '//vip.' not in resp['link']:
        raise Exception("api error: not a VIP link")
    return resp['link']
