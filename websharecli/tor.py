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
