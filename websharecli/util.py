from websharecli.exceptions import InvalidUrlException
from websharecli.terminal import T

from itertools import cycle, islice
from collections import Counter
import os

SYMBOLS = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')


def bytes2human(n):
    """Convert n bytes to a human readable value of 4 characters."""
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    prefix = {}
    for i, s in enumerate(SYMBOLS):
        prefix[s] = 1 << i*10
    for symbol in reversed(SYMBOLS):
        value = float(n) / prefix[symbol]
        if 999 >= value > 0.9:
            if value <= 9.9:
                return f"{value:1.1f}{symbol}"
            else:
                return f"{value:3.0f}{symbol}"


def repeat_list_to_length(lst, length):
    # Use itertools.cycle to create an iterator that cycles through the list indefinitely
    repeated_list = cycle(lst)
    # Use islice to slice the repeated_list to the desired length
    return list(islice(repeated_list, length))


def distinguish_filenames(filenames):
    # Count occurrences of each filename
    filename_counts = Counter(filenames)

    # Create a dictionary to store filename occurrences
    filename_occurrences = {}

    # Iterate over filenames and append a unique identifier
    new_filenames = []
    for i, filename in enumerate(filenames):
        count = filename_counts[filename]
        if count > 1:
            if filename not in filename_occurrences:
                filename_occurrences[filename] = 1
            else:
                filename_occurrences[filename] += 1
            # Append unique identifier to filename
            name, extension = os.path.splitext(filename)
            new_filename = f"{name}_{filename_occurrences[filename]}{extension}"
            new_filenames.append(new_filename)
        else:
            new_filenames.append(filename)
    return new_filenames


def remove_duplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]


def ident_from_url(url):
    try:
        # https://webshare.cz/#/file/30lWR3a77h/requiem-for-a-dream-en-dvdrip-avi -> 30lWR3a77h
        _, right = url.split("/file/")
        return right.split("/")[0]
    except Exception as exc:
        print(f"{T.red}invalid url, use url such as https://webshare.cz/#/file/4jw52F2kv4/mocny-vladce-oz-2013-cz-dabing-brrip-xvid-avi{T.normal}")
        raise InvalidUrlException(exc)


def filename_from_url(url):
    try:
        # https://free.5.dl.wsfiles.cz/1104/4j47jd5X95/300000/eJw1js1OxCAURt_lLlwB5a8gJBMfwKSujC66gQIzTJqOobSaGt9dNJndzf3u+c79BgcWpCJcEEWJBgQZLEVQwTJNjdRGMIlg_19uYJdtnhGsLUXwATa5eY0IllZyLm7P1U3Z4fsY8XTg4HxezphTJvHXngNpWdOEhoiYmFHJJ8q81k49Oh9U0wojQ0jecMG1lor_nde7uzTwM_r14kok0zF2Kc9x7ORV6mvo300_dk+xlFs5vQ7Pw8vb8HA7tYLauFq29ux6gNWC970WjP_8AhJHSeg/ea97ae17fd7f12945faf6b798b18282e4969232d/gravitacia-gravitace-cz-dabing-2014-xvid.avi
        return url.rsplit("/", 1)[-1]
    except Exception as exc:
        print(f"{T.red}invalid url, use url such as https://free.5.dl.wsfiles.cz/1104/4j47jd5X95/300000/eJw1js1OxCAURt_lLlwB5a8gJBMfwKSujC66gQIzTJqOobSaGt9dNJndzf3u+c79BgcWpCJcEEWJBgQZLEVQwTJNjdRGMIlg_19uYJdtnhGsLUXwATa5eY0IllZyLm7P1U3Z4fsY8XTg4HxezphTJvHXngNpWdOEhoiYmFHJJ8q81k49Oh9U0wojQ0jecMG1lor_nde7uzTwM_r14kok0zF2Kc9x7ORV6mvo300_dk+xlFs5vQ7Pw8vb8HA7tYLauFq29ux6gNWC970WjP_8AhJHSeg/ea97ae17fd7f12945faf6b798b18282e4969232d/gravitacia-gravitace-cz-dabing-2014-xvid.avi{T.normal}")
        raise InvalidUrlException(exc)


def makedir(dest_dir):
    if dest_dir:
        if os.path.isabs(dest_dir): # absolute path /home/user/some/folder
            path = dest_dir
        else:
            path = os.path.join(os.getcwd(), dest_dir)
        if not os.path.exists(path):
            os.makedirs(path)
        elif os.path.isfile(path):  # existing file, raise error
            raise FileExistsError(f"Cannot create destination folder {path}, already a file")
