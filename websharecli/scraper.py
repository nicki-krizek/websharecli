import requests
import bs4
from websharecli.util import ident_from_url
from websharecli.api import file_link_by_id
from websharecli.exceptions import WebshareCliException
from websharecli.terminal import T


def url(query, page_num):
    return f"https://webshare.cz/search?what={query}&page={page_num}"


def get_download_link(file_url, ignore_vip):
    ident = ident_from_url(file_url)
    download_link = file_link_by_id(ident, ignore_vip=ignore_vip)
    return download_link


def scrape_page_download_links(query, page_num, ignore_vip):
    html = requests.get(url(query, page_num)).text
    soup = bs4.BeautifulSoup(html, "lxml")
    h2_elements = soup.find_all('h2')
    # Iterate through each <h2> element and find the <a> element inside
    download_links = []
    unavailable_links = []
    for h2 in h2_elements:
        a_tag = h2.find('a')  # Find the <a> tag inside the <h2> element
        if a_tag:
            file_url = a_tag.get('href')  # Get the value of the 'href' attribute
            if type(file_url) is str and file_url.startswith("/file/"):
                try:
                    download_link = get_download_link(file_url, ignore_vip)
                    download_links.append(download_link)
                except WebshareCliException:
                    # print(f"{T.red}unable to get download link of {file_url}, skipping{T.normal}")
                    unavailable_links.append(file_url)
    return download_links, unavailable_links


def scrape_all_pages_download_links(query, ignore_vip):
    download_links = []
    unavailable_links = []
    page_num = 1
    while True:
        dlinks, ulinks = scrape_page_download_links(query, page_num, ignore_vip)
        if not (dlinks + ulinks):   # no links
            break
        download_links += dlinks.copy()
        unavailable_links += ulinks.copy()
        page_num += 1
    return download_links, unavailable_links


def main():
    download_links, unavailable_links = scrape_all_pages_download_links("gravitace mkv", False)
    print(len(download_links), unavailable_links)


if __name__ == '__main__':
    main()
