import os
import threading
from tqdm import tqdm
from websharecli.util import filename_from_url

# Set up proxies
proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}


# Function to make a GET request through Tor
def make_requests_tor_session():
    import requests
    session = requests.Session()
    session.proxies.update(proxies)
    return session


def download_file(url, output_path):
    print("Downloading file...")
    session = make_requests_tor_session()
    response = session.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024*8  # 8 KB

    progress_bar = tqdm(total=total_size_in_bytes, unit='B', unit_scale=True, desc=os.path.basename(output_path))
    with open(output_path, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("Error: Download incomplete.")

    print("File downloaded successfully!")


def download(urls, output_folder):
    # Make requests in parallel using threads
    threads = []
    for url in urls:
        output_path = os.path.join(output_folder, filename_from_url(url))
        thread = threading.Thread(target=download_file, args=(url, output_path))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    urls = ["https://free.1.dl.wsfiles.cz/7174/78w13o72e8/300000/eJw1j01LxTAQRf9KmIUo5LVJGpK28HDjRoQKgrjpJm0mbaCvremXPvG_GwW3c+cezv0CAyVIlYgsUSzRQMFDySisUHLNCqkLoSSF_e+4QTluw0BhiSmFGUpnhgUpjBHC+QfT5GGyHZLRkGU2Q+vb_sTJ7Qu+bx4vxE2BGNL2uH8e6Lt+JY93xO42+PnUdyG5zDIK2AjL0PFCucYx3mhtVG4aq6JQVkhrXVOITGgtlfh9X_+tQiwe2Cy9CZi01zp1fsA61fnBs0kLzOv0HkOYwvm1eqqe36qb6RwBa+ytYYszlmvcxRXLuRb59w_XBFGj/c801edec6aff0146df93d7c59b0fc7327507dd7f/11x07-Dodge-na-spalcich-1-Requiem-for-a-chevyweight-I-dvdrip-hgr.mp4",
            "https://free.5.dl.wsfiles.cz/1104/4j47jd5X95/300000/eJw1js1OxCAURt_lLlwB5a8gJBMfwKSujC66gQIzTJqOobSaGt9dNJndzf3u+c79BgcWpCJcEEWJBgQZLEVQwTJNjdRGMIlg_19uYJdtnhGsLUXwATa5eY0IllZyLm7P1U3Z4fsY8XTg4HxezphTJvHXngNpWdOEhoiYmFHJJ8q81k49Oh9U0wojQ0jecMG1lor_nde7uzTwM_r14kok0zF2Kc9x7ORV6mvo300_dk+xlFs5vQ7Pw8vb8HA7tYLauFq29ux6gNWC970WjP_8AhJHSeg/ea97ae17fd7f12945faf6b798b18282e4969232d/gravitacia-gravitace-cz-dabing-2014-xvid.avi"]
    folder = "/mnt/data/Download/"
    download(urls, folder)