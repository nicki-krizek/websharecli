import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from websharecli.util import filename_from_url, repeat_list_to_length, distinguish_filenames, ident_from_download_link
from websharecli.tor import make_requests_tor_session, make_urlretrieve_tor
from websharecli.api import file_link_by_id
from websharecli.terminal import T
from websharecli.exceptions import TooManyDownloadRetriesException
from websharecli import config
from websharecli.progress import ProgressBar


def download_url(url, output_path, tor, tor_port, i=1, n=1, retries=3, timeout=10):
    session, original_ip, tor_ip = make_requests_tor_session(tor, tor_port)
    if tor:
        # print(f"{T.green}Downloading file through tor proxies (http / https) {' / '.join(session.proxies.values())}"
        #       f", original ip: {original_ip}; tor ip: {tor_ip}{T.normal}", file=sys.stderr)
        pbar_desc = f"{i}/{n} {T.magenta}(TOR:{tor_ip}){T.normal} {os.path.basename(output_path)}"
        assert original_ip != tor_ip, "Traffic is not going through tor. Exit."
    else:
        # print(f"{T.yellow}Downloading file without tor, your ip: {original_ip}{T.normal}", file=sys.stderr)
        pbar_desc = f"{i}/{n}{T.normal} {os.path.basename(output_path)}"
    response = session.get(url, stream=True, allow_redirects=True, headers={"Connection": "close"})
    total_size_in_bytes = int(response.headers.get('content-length', 0))

    progress_bar = tqdm(desc=pbar_desc, total=total_size_in_bytes, unit='B', unit_scale=True)
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=config.CONFIG.chunk_size):
            if chunk:
                progress_bar.update(len(chunk))
                f.write(chunk)

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        # print("Error: Download incomplete. Try again", file=sys.stderr)
        # clear current attempt
        session.close()
        os.remove(output_path)
        time.sleep(timeout)
        # try again
        ident = ident_from_download_link(url)
        url = file_link_by_id(ident)
        retries -= 1
        if retries > 0:
            progress_bar.desc = f"{T.red}RETRY{T.normal} " + progress_bar.desc
            progress_bar.close()

            return download_url(url, output_path, tor, tor_port, i, n, retries, timeout)
        else:
            # print("Download incomplete. No more retries.", file=sys.stderr)
            progress_bar.desc = f"{T.red}FAIL{T.normal} " + progress_bar.desc
            progress_bar.close()
            raise TooManyDownloadRetriesException(f"Unable to download {url}. Tried {retries} times.")
    else:
        progress_bar.desc = f"{T.green}SUCCESS{T.normal} " + progress_bar.desc
        progress_bar.close()
        # print("File downloaded successfully!", file=sys.stderr)


def download_url_urlretrive(url, output_path, tor, tor_port, i=1, n=1):
    urlretrieve, original_ip, tor_ip = make_urlretrieve_tor(tor, tor_port)
    filename = os.path.basename(output_path)
    if tor:
        pbar_desc = f"{i}/{n} {T.magenta}(TOR):{tor_ip}{T.normal} {filename}"
        assert original_ip != tor_ip, "Traffic is not going through tor. Exit."
    else:
        pbar_desc = f"{i}/{n}{T.normal} {filename}"

    (local_filename, headers) = urlretrieve(url, output_path, ProgressBar(pbar_desc))


def download_urls(urls, output_folder, tor, tor_ports, pool_size):
    output_paths = list(map(lambda x: os.path.join(output_folder, filename_from_url(x)), urls))
    output_paths = distinguish_filenames(output_paths)
    tors = [tor] * len(urls)
    ports_for_each_url = repeat_list_to_length(tor_ports, len(urls))
    i_list = range(1, len(urls) + 1)
    n_list = [len(urls)] * len(urls)
    with ThreadPoolExecutor(max_workers=pool_size) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(download_url_urlretrive, url, output_path, tor, tor_port, i, n)
                   for (url, output_path, tor, tor_port, i, n) in
                   zip(urls, output_paths, tors, ports_for_each_url, i_list, n_list)]
        # Use as_completed to get the results as they are completed
        for future in as_completed(futures):
            result = future.result()


def multi_parts_test():
    import requests
    url = "https://free.5.dl.wsfiles.cz/1104/4j47jd5X95/300000/eJw1jslKxEAQht+lDp46SS_pJQ2DDyDEk+ghIDXpzthDSKSzjER8d2sEb8X3L_V_A4KH2pRSlYaXFhgk8JzBCl5Y3jSaK+EY7H9wAz9t48hgIZXBJ_gBxyUymKjkknFPK_YJi_8zFv1RBDyn6VJILuria0+hJI3eBIq4YTBchIYrI6NzKDjGHqMxTlt0jQiK8x6ludtpEAxpjO9hvk3jjIFgJnaL5+UDcyz7o6vuhq6qr7W9Bv3W6K56jDnP+fTSPrXPr+3DfKLYSrk1b7R7OcBbJbW2SsifX26xTbo/4d2bb18d99aecc26c2548b3407c8b8aefadc22e4/gravitacia-gravitace-cz-dabing-2014-xvid.avi"
    start = 0
    size = 10e6
    response = requests.get(url, stream=True, allow_redirects=True, headers={f"Range": f"bytes={start}-{size}", "Connection": "close"})
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    print(response.status_code)
    with open("/mnt/data/Download/TRASH/test.bin", 'wb') as f:
        for chunk in response.iter_content(chunk_size=config.CONFIG.chunk_size):
            if chunk:
                f.write(chunk)


if __name__ == '__main__':
    multi_parts_test()
