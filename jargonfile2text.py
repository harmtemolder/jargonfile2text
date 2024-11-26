#!/usr/bin/env python3


import requests
import zipfile
import io

from pathlib import Path


def download(repo):
    url = f'https://github.com/{repo}/zipball/main'
    print(f'Downloading {url}...')
    r = requests.get(url, stream=True)

    if not r.ok:
        raise ConnectionError

    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall('in')


def main(repo, path):
    if not Path('in').is_dir():
        download(repo)

    pass


if __name__ == '__main__':
    main(
        repo='agiacalone/jargonfile',
        path='html'
    )
