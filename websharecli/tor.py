import requests
import socks
import socket
import urllib.request as req

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


# Set up proxies
def proxies(port):
    return {
        'http': f'socks5h://localhost:{port}',
        'https': f'socks5h://localhost:{port}'
    }


# Function to make a GET request through Tor
def make_requests_tor_session(tor, port):
    import requests
    session = requests.Session()
    original_ip = get_public_ip(session)
    if tor:
        session.proxies.update(proxies(port))
    tor_ip = get_public_ip(session)
    return session, original_ip, tor_ip


def get_public_ip(session):
    response = session.get('https://api.ipify.org?format=json')
    if response.status_code == 200:
        data = response.json()
        return data['ip']
    else:
        return None


def get_public_ip_requests():
    response = requests.get('https://api.ipify.org?format=json')
    if response.status_code == 200:
        data = response.json()
        return data['ip']
    else:
        return None


def make_urlretrieve_tor(tor, port):
    original_ip = get_public_ip_requests()
    if tor:
        proxy_ip = "127.0.0.1"
        proxy_port = port
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, proxy_ip, proxy_port)
        socket.socket = socks.socksocket

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()

    opener = req.build_opener()
    opener.addheaders = [('User-Agent', user_agent)]
    req.install_opener(opener)
    tor_ip = get_public_ip_requests()

    return req.urlretrieve, original_ip, tor_ip


if __name__ == '__main__':
    urlretrieve, original_ip, tor_ip = make_urlretrieve_tor(True, 9050)
    filename, header = urlretrieve("https://api.ipify.org", "abc.txt")
    print(header)
