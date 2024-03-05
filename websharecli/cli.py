#!/usr/bin/python3
import argparse
import os
import shutil
import sys

from websharecli import api
from websharecli import config
from websharecli import commands
from websharecli.terminal import T
from websharecli.util import ident_from_url, filename_from_url, remove_duplicates, makedir
from websharecli.downloader import download_url, download_urls
from websharecli.scraper import scrape_all_pages_download_links


def link_search(args):
    query = ' '.join(args.what)
    files, links = commands.link_search(
            query,
            exclude=args.exclude,
            ignore_vip=args.ignore_vip,
            verbose=args.verbose)
    for link, filename in zip(files, links):
        if args.download:
            if args.tor_port:
                download_url(link, filename, tor=True, tor_port=args.tor_port)
            else:
                download_url(link, filename, tor=args.tor, tor_port=config.CONFIG.tor_port)
        else:
            print(link)


def link_list(args):
    query = ' '.join(args.what)
    files = commands.link_list(
        query,
        exclude=args.exclude,
        limit=args.limit)
    for i, file in enumerate(files):
        print(f"{i+1:2d}. {file}", file=sys.stderr)


def get_link_by_id(args):
    try:
        link = api.file_link_by_id(args.id, ignore_vip=args.ignore_vip)
        if args.download:
            filename = filename_from_url(link)  # FIXME not pretty, make use of data.File
            if args.tor_port:
                download_url(link, filename, tor=True, tor_port=args.tor_port)
            else:
                download_url(link, filename, tor=args.tor, tor_port=config.CONFIG.tor_port)
        else:
            print(link)
    except api.LinkUnavailableException as exc:
        print(f'{T.red}{exc}{T.normal}', file=sys.stderr)
        sys.exit(1)


def get_link_by_url(args):
    try:
        ident = ident_from_url(args.url)
        link = api.file_link_by_id(ident, ignore_vip=args.ignore_vip)
        if args.download:
            filename = filename_from_url(link)  # FIXME not pretty, make use of data.File
            if args.tor_port:
                download_url(link, filename, tor=True, tor_port=args.tor_port)
            else:
                download_url(link, filename, tor=args.tor, tor_port=config.CONFIG.tor_port)
        else:
            print(link)
    except api.LinkUnavailableException as exc:
        print(f'{T.red}{exc}{T.normal}', file=sys.stderr)
        sys.exit(1)


def link_scrape(args):
    query = ' '.join(args.what)
    download_links, unavailable_links = scrape_all_pages_download_links(query, args.ignore_vip)
    if args.skip_same:
        download_links = remove_duplicates(download_links)
    if args.download:
        dest_dir = args.dest_dir if args.dest_dir and args.dest_dir.strip() else ""
        makedir(dest_dir)
        if args.tor_ports:
            if args.pool:
                download_urls(download_links, dest_dir, True, args.tor_ports, args.pool)
            else:
                download_urls(download_links, dest_dir, True, args.tor_ports, config.CONFIG.pool_size)
        else:
            download_urls(download_links, dest_dir, args.tor, [config.CONFIG.tor_port], config.CONFIG.pool_size)
    else:
        print("\n".join(download_links))


def sample_config(args):
    if os.path.exists(config.CONFIG_FILE):
        print(f"{T.red}Configuration file already exists in {config.CONFIG_FILE}{T.normal}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(os.path.dirname(config.CONFIG_FILE), exist_ok=True)
    shutil.copy(
        config.CONFIG_FILE_TEMPLATE,
        config.CONFIG_FILE
    )
    print(
        "{T.yellow}Customize the config file to enable VIP or change default quality:\n"
        "{config.CONFIG_FILE}{T.normal}",
        file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='webshare.cz API client')
    subparsers = parser.add_subparsers(help='choose a subcomand',
                                       dest='subparser')

    link_search_parser = subparsers.add_parser('link-search', help='find and download file')
    link_search_parser.add_argument(
        '-s', '--silent', action='store_false', dest='verbose',
        help='disable status prints to stderr')
    link_search_parser.add_argument(
        '-x', '--exclude', type=str, action='append',
        help='exclude results matching phrase (case-insensitive)')
    link_search_parser.add_argument(
        '--ignore-vip', action='store_true',
        help='override force_vip configuration and temporarily allow non-vip links')
    link_search_parser.add_argument(
        '--download', action='store_true', help='download the searched link')
    link_search_parser.add_argument(
        '--tor', action='store_true', help='download through tor')
    link_search_parser.add_argument(
        '--tor-port', type=int, help='download through specific tor port')
    link_search_parser.add_argument(
        'what', type=str, nargs='+',
        help='string identifying the file (use "*" to search for 00-99)')

    link_list_parser = subparsers.add_parser('link-list', help='search for files')
    link_list_parser.add_argument(
        '-l', '--limit', type=int, help='limit the number of results')
    link_list_parser.add_argument(
        '-x', '--exclude', type=str, action='append',
        help='exclude results matching phrase (case-insensitive)')
    link_list_parser.add_argument(
        'what', type=str, nargs='+', help='string identifying the file')

    link_id_parser = subparsers.add_parser('link-id', help='get downloadable link from file id')
    link_id_parser.add_argument(
        '--ignore-vip', action='store_true',
        help='override force_vip configuration and temporarily allow non-vip links')
    link_id_parser.add_argument(
        '--download', action='store_true', help='download the searched link')
    link_id_parser.add_argument(
        '--tor', action='store_true', help='download through tor')
    link_id_parser.add_argument(
        '--tor-port', type=int, help='download through specific tor port')
    link_id_parser.add_argument(
        'id', type=str, help='ID of the file')

    link_url_parser = subparsers.add_parser('link-url', help='get downloadable link from file url')
    link_url_parser.add_argument(
        '--ignore-vip', action='store_true',
        help='override force_vip configuration and temporarily allow non-vip links')
    link_url_parser.add_argument(
        '--download', action='store_true', help='download the searched link')
    link_url_parser.add_argument(
        '--tor', action='store_true', help='download through tor')
    link_url_parser.add_argument(
        '--tor-port', type=int, help='download through specific tor port')
    link_url_parser.add_argument(
        'url', type=str, help='url of the file')

    link_scrape_parser = subparsers.add_parser('link-scrape', help='search for files and scrape download links')
    # link_scrape_parser.add_argument(
    #     '-s', '--silent', action='store_false', dest='verbose',
    #     help='disable status prints to stderr')
    # link_scrape_parser.add_argument(
    #     '-x', '--exclude', type=str, action='append',
    #     help='exclude results matching phrase (case-insensitive)')
    link_scrape_parser.add_argument(
        '--ignore-vip', action='store_true',
        help='override force_vip configuration and temporarily allow non-vip links')
    link_scrape_parser.add_argument(
        '--download', action='store_true', help='download the searched link')
    link_scrape_parser.add_argument(
        '--tor', action='store_true', help='download through tor')
    link_scrape_parser.add_argument(
        '--tor-ports', nargs='+', type=int, help='download through specific tor port')
    link_scrape_parser.add_argument(
        '--dest-dir', type=str, help='destination directory to save downloaded files to')
    link_scrape_parser.add_argument(
        '--pool', type=int, help='the size of the threading pool, how many files download at the same time')
    link_scrape_parser.add_argument(
        '--skip-same', action='store_true', help='skip downloading files with identical filename')
    link_scrape_parser.add_argument(
        'what', type=str, nargs='+',
        help='string identifying the files')

    subparsers.add_parser(
        'sample-config', help='create sample config file')

    args = parser.parse_args()
    if args.subparser is None:
        parser.print_help()
        sys.exit(1)

    functions = {
        'link-search': link_search,
        'link-list': link_list,
        'link-id': get_link_by_id,
        'link-url': get_link_by_url,
        'link-scrape': link_scrape,
        'sample-config': sample_config,
    }
    try:
        functions[args.subparser](args)
    except api.NotVipLinkException:
        print(
            f"{T.red}ERROR: Received non-VIP link. Possible causes:\n"
            "  - wst token expired - re-login and update config\n"
            "  - VIP membership expired - renew membership and token\n"
            f"  - unrelated/temporary error - use --ignore-vip{T.normal}",
            file=sys.stderr)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
