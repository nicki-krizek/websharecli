from webshare import api
from webshare.config import CONFIG
from webshare.data import File, filter_unique


def download(what, verbose=False):
    """Get download link(s) for files that match the search query"""
    results = []
    files = search(what, limit=1)
    if files:
        results.append(api.file_link(files[0].ident))
    elif verbose:
        print(
            'Nothing found for: "{query}"'.format(query=' '.join(what)),
            file=sys.stderr)  # noqa
    return results


def search(what, limit=None):
    """Search and filter results based on quality."""
    query = ' '.join(what)
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
