#!/usr/bin/python3
import argparse
import os
import shutil
import sys

from websharecli import api
from websharecli import config
from websharecli import commands


def download(args):
    query = ' '.join(args.what)
    for link in commands.download(query, verbose=args.verbose):
        print(link)


def search(args):
    query = ' '.join(args.what)
    files = commands.search(query, limit=args.limit)
    for i, file in enumerate(files):
        print("{:2d}. {}".format((i+1), file))


def get_link(args):
    data = api.file_link(args.id)
    print(data)


def sample_config(args):
    if os.path.exists(config.CONFIG_FILE):
        print("Configuration file already exists in {path}".format(
            path=config.CONFIG_FILE))
        sys.exit(1)
    os.makedirs(os.path.dirname(config.CONFIG_FILE), exist_ok=True)
    shutil.copy(
        config.CONFIG_FILE_TEMPLATE,
        config.CONFIG_FILE
    )
    print(
        "Customize the config file to enable VIP or change default quality:\n"
        "{path}".format(path=config.CONFIG_FILE))


def main():
    parser = argparse.ArgumentParser(description='webshare.cz API client')
    subparsers = parser.add_subparsers(help='choose a subcomand',
                                       dest='subparser')

    download_parser = subparsers.add_parser(
        'download', help='find and download file')
    download_parser.add_argument(
        '-s', '--silent', action='store_false', dest='verbose',
        help='disable status prints to stderr')
    download_parser.add_argument(
        'what', type=str, nargs='+',
        help='string identifying the file (use "*" to search for 00-99)')

    search_parser = subparsers.add_parser('search', help='search for files')
    search_parser.add_argument(
        '-l', '--limit', type=int, help='limit the number of results')
    search_parser.add_argument(
        'what', type=str, nargs='+', help='string identifying the file')

    link_parser = subparsers.add_parser('link', help='get downloadable link')
    link_parser.add_argument(
        'id', type=str, help='ID of the file')

    subparsers.add_parser(
        'sample-config', help='create sample config file')

    args = parser.parse_args()
    if args.subparser is None:
        parser.print_help()
        sys.exit(1)

    functions = {
        'download': download,
        'search': search,
        'link': get_link,
        'sample-config': sample_config,
    }
    functions[args.subparser](args)


if __name__ == '__main__':
    main()
