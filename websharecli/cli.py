#!/usr/bin/python3
import argparse
import os
import shutil
import sys

from websharecli import api
from websharecli import config
from websharecli import commands
from websharecli.terminal import T
from websharecli.util import ident_from_url
from websharecli.downloader import download_url, download_urls


def link_search(args):
    query = ' '.join(args.what)
    links, filenames = commands.link_search(
            query,
            exclude=args.exclude,
            ignore_vip=args.ignore_vip,
            verbose=args.verbose)
    for link, filename in zip(links, filenames):
        if args.download:
            download_url(link, filename, args.tor)
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
        data = api.file_link(args.id, ignore_vip=args.ignore_vip)
    except api.LinkUnavailableException as exc:
        print(f'{T.red}{exc}{T.normal}', file=sys.stderr)
        sys.exit(1)
    print(data)


def get_link_by_url(args):
    try:
        ident = ident_from_url(args.url)
        data = api.file_link(ident, ignore_vip=args.ignore_vip)
    except api.LinkUnavailableException as exc:
        print(f'{T.red}{exc}{T.normal}', file=sys.stderr)
        sys.exit(1)
    print(data)


def sample_config(args):
    if os.path.exists(config.CONFIG_FILE):
        print(
            f"{T.red}Configuration file already exists in {config.CONFIG_FILE}{T.normal}",
            file=sys.stderr)
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
        'id', type=str, help='ID of the file')
    link_id_parser.add_argument(
        '--download', action='store_true', help='download the searched link')

    link_url_parser = subparsers.add_parser('link-url', help='get downloadable link from file url')
    link_url_parser.add_argument(
        '--ignore-vip', action='store_true',
        help='override force_vip configuration and temporarily allow non-vip links')
    link_url_parser.add_argument(
        'url', type=str, help='url of the file')
    link_url_parser.add_argument(
        '--download', action='store_true', help='download the searched link')

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
