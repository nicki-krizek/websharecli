import argparse
import sys

from webshare import api
from webshare.data import File


def search(args):
    data = api.search(' '.join(args.what))
    files = [File(**entry) for entry in data]
    for i, file in enumerate(files):
        print("{:2d}. {}".format((i+1), file))


def get_link(args):
    data = api.file_link(args.id)
    print(data)


def main():
    parser = argparse.ArgumentParser(description='webshare.cz API client')
    subparsers = parser.add_subparsers(help='choose a subcomand',
                                       dest='subparser')

    search_parser = subparsers.add_parser('search', help='search for files')
    search_parser.add_argument(
        'what', type=str, nargs='+', help='string identifying the file')

    link_parser = subparsers.add_parser('link', help='get downloadable link')
    link_parser.add_argument(
        'id', type=str, help='ID of the file')

    args = parser.parse_args()
    if args.subparser is None:
        parser.print_help()
        sys.exit(1)

    functions = {
        'search': search,
        'link': get_link,
    }
    functions[args.subparser](args)


if __name__ == '__main__':
    main()
