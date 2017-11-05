import sys

from websharecli import api
from websharecli.config import CONFIG
from websharecli.data import File, filter_unique


def download(query, verbose=False):
    """Get download link(s) for files that match the search query"""
    results = []
    not_found = 0
    for q in query_complete_wildcard(query):
        files = search(q, limit=1)
        report = '{query}: {res}'
        if files:
            not_found = 0
            results.append(api.file_link(files[0].ident))
            print(report.format(query=q, res=files[0].name),
                  file=sys.stderr)  # noqa
        else:
            not_found += 1
            print(
                report.format(query=q, res="NOT FOUND"),
                file=sys.stderr)  # noqa
        if not_found >= 3:
            if verbose:
                print('Aborting after 3 failures', file=sys.stderr)  # noqa
            break
    return results


def search(query, limit=None):
    """Search and filter results based on quality."""
    results = filter_unique(get_files(query))
    if limit:
        results = results[:limit]
    return results


def get_files(query):
    """Perform query for every configured quality and return all results"""
    results = []
    for q in query_expand(query, CONFIG.quality):
        for entry in api.search(q):
            file_ = File(**entry)
            if file_.matches_query(q):
                results.append(file_)
    return results


def normalize_query(query):
    """Lowercase words and use only unique ones"""
    normalized = []
    for word in query.split(' '):
        word = word.lower()
        if word and word not in normalized:
            normalized.append(word)
    return ' '.join(normalized)


def query_expand(query, options=None):
    """Create multiple queries by extending it by some options"""
    query = normalize_query(query)
    if not options:
        return [query]
    results = []
    for option in options:
        results.append(normalize_query(query + ' ' + option))
    return results


def query_complete_wildcard(query):
    """Find asterisk ('*') and replace with numbers from 00 to 99"""
    if '*' not in query:
        return [query]
    return ['{}'.format(
        query.replace('*', '{:02d}'.format(i))) for i in range(100)]
