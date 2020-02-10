import os
import requests


def download_file(url, path="/tmp"):
    """
    Download a file to the given path
    """

    fname = url.split("/")[-1]
    path = os.path.join(path, fname)

    r = requests.get(url, stream=True)

    with open(path, "wb") as f:

        for ch in r:

            f.write(ch)
    return path
