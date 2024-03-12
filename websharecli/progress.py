from tqdm import tqdm
from websharecli.terminal import T


class ProgressBar(object):

    def __init__(self, desc):
        self.desc = desc
        self.pbar = None
        self.downloaded = 0
        self.total_size = 0

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar = tqdm(desc=self.desc, total=total_size, unit='B', unit_scale=True)
            self.total_size = total_size

        self.downloaded = block_num * block_size
        if self.downloaded < self.total_size:
            self.pbar.update(block_size)
        else:
            self.finished()

    def finished(self):
        self.pbar.desc = f"{T.green}SUCCESS{T.normal} " + self.pbar.desc
        self.pbar.close()


def main():
    import socks
    import socket
    import urllib.request as req

    from random_user_agent.user_agent import UserAgent
    from random_user_agent.params import SoftwareName, OperatingSystem

    proxy_ip = "127.0.0.1"
    proxy_port = 9050

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()

    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, proxy_ip, proxy_port)
    socket.socket = socks.socksocket

    proxy = req.ProxyHandler({})
    opener = req.build_opener(proxy)
    opener.addheaders = [('User-Agent', user_agent)]
    req.install_opener(opener)

    url = "https://free.1.dl.wsfiles.cz/7212/P7af3632y3/300000/eJw1j0tPwzAQhP_LHjilG6+d2kmkChXKQ0IJVdoCh1wcYouI0FTOA6WI_45B4rqz883MF2hIgSKFXBByQlIKAmggZQEMkJIiRkouZRLA9HccIT2ObRtA79UATpBa3fYmgKMH3Tk9NcOMnJHAq3Ys9IzEYnbCzX63uN9gtsYlEq6frrG4yQ4vi1unM7PbdwW+nvHjffLhtQcJYymRtrKMKqW0jHVVS1JMJFFd2yrhgisVSf77Pvw3ct74aar+TTvjcWVom9aU4VZpK6TgsyjDS+Nc51aH_CF_fM4vupUHDN43uNFP6M9+k4wjxigizr9_AD6kTtY/d97285159f3c409d8f1f1ac4a78a22d7b18a895d/Gravity.2013.BluRay.1080p.DTS-HD.MA.5.1.AVC.REMUX-FraMeSToR.cz.mkv"
    filename = "/mnt/data/Download/TRASH/abc.mp4"
    (local_filename, headers) = req.urlretrieve(url, filename, ProgressBar(filename))


if __name__ == '__main__':
    main()
