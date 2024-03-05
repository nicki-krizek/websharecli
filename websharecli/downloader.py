import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from websharecli.util import filename_from_url, repeat_list_to_length, distinguish_filenames
from websharecli.tor import make_requests_tor_session
from websharecli.terminal import T
from websharecli import config


def download_url(url, output_path, tor, tor_port):
    session, original_ip, tor_ip = make_requests_tor_session(tor, tor_port)
    if tor:
        print(f"{T.green}Downloading file through tor proxies (http / https) {' / '.join(session.proxies.values())}"
              f", original ip: {original_ip}; tor ip: {tor_ip}{T.normal}", file=sys.stderr)
        assert original_ip != tor_ip, "Traffic is not going through tor. Exit."
    else:
        print(f"{T.yellow}Downloading file without tor, your ip: {original_ip}{T.normal}", file=sys.stderr)
    response = session.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = config.CONFIG.chunk_size  # ~1 KB

    progress_bar = tqdm(total=total_size_in_bytes, unit='B', unit_scale=True, desc=os.path.basename(output_path))
    with open(output_path, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("Error: Download incomplete. Try again", file=sys.stderr)
        session.close()
        os.remove(output_path)
        time.sleep(1)
        return download_url(url, output_path, tor, tor_port)

    print("File downloaded successfully!")


def download_urls(urls, output_folder, tor, tor_ports, pool_size):
    output_paths = list(map(lambda x: os.path.join(output_folder, filename_from_url(x)), urls))
    output_paths = distinguish_filenames(output_paths)
    tors = [tor]*len(urls)
    ports_for_each_url = repeat_list_to_length(tor_ports, len(urls))
    with ThreadPoolExecutor(max_workers=pool_size) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(download_url, url, output_path, tor, tor_port)
                   for (url, output_path, tor, tor_port) in zip(urls, output_paths, tors, ports_for_each_url)]
        # Use as_completed to get the results as they are completed
        for future in as_completed(futures):
            result = future.result()
