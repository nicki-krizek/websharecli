#!/usr/bin/python3
import argparse
import sys

from webshare import api
from webshare import commands


def search(args):
    files = commands.search(args.what, limit=args.limit)
    for i, file in enumerate(files):
        print("{:2d}. {}".format((i+1), file))


def get_link(args):
    data = api.file_link(args.id)
    print(data)


def sample_config(args):
    print(
        "# ~/.config/webshare/config.yaml\n\n"
        "headers:\n"
        "  Cookie: wst=xxxxx\n"
        "  User-Agent: XXXX\n"
        "force_vip: true\n"
        "quality:\n"
        "  - 1080p\n"
        "  - 720p"
    )


def main():
    parser = argparse.ArgumentParser(description='webshare.cz API client')
    subparsers = parser.add_subparsers(help='choose a subcomand',
                                       dest='subparser')

    search_parser = subparsers.add_parser('search', help='search for files')
    search_parser.add_argument(
        '-l', '--limit', type=int, help='limit the number of results')
    search_parser.add_argument(
        'what', type=str, nargs='+', help='string identifying the file')

    link_parser = subparsers.add_parser('link', help='get downloadable link')
    link_parser.add_argument(
        'id', type=str, help='ID of the file')

    subparsers.add_parser(
        'sample-config', help='show configuration file example')

    args = parser.parse_args()
    if args.subparser is None:
        parser.print_help()
        sys.exit(1)

    functions = {
        'search': search,
        'link': get_link,
        'sample-config': sample_config,
    }
    functions[args.subparser](args)


if __name__ == '__main__':
    main()
