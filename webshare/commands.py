from webshare import api
from webshare.config import CONFIG
from webshare.data import File


def search(what):
    """Search and filter results based on quality."""
    results = []
    search_term = ' '.join(what)

    for quality in CONFIG.quality:
        data = api.search(search_term + ' ' + quality)
        files = [File(**entry) for entry in data]
        must_match = list(what)
        must_match.append(quality)
        must_match = [word.upper() for word in must_match]
        for file_ in files:
            file_name = file_.name.upper()
            if all([word in file_name for word in must_match]):
                results.append(file_)

    return results
