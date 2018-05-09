#!/usr/bin/env python

from __future__ import print_function, unicode_literals

from bs4 import BeautifulSoup
import os
import requests
import shutil
import sys
import subprocess
import urlparse


def fetch_html(url):
    req = requests.get(url + '?raw')
    req.raise_for_status()
    body = req.text
    req = requests.get(url + '$json')
    req.raise_for_status()
    j = req.json()
    title = j['title']
    slug = j['slug'].split('/')[-1]
    return body, title, slug


def download_file(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)


def main():
    url = sys.argv[1]
    out_path = sys.argv[2]
    if not os.path.exists(out_path):
        os.mkdirs(out_path)
    body, title, slug = fetch_html(url)
    document = BeautifulSoup(body, 'html.parser')
    for i in document.find_all('img'):
        img = i.get('src')
        u = urlparse.urlparse(img)
        name = os.path.basename(u.path)
        img_url = urlparse.urljoin(url, img)
        print('Downloading image {}'.format(img_url))
        download_file(img_url, os.path.join(out_path, name))
        i['src'] = name
    html_bytes = document.prettify().encode('utf-8')
    out = os.path.join(out_path, slug + '.rst')
    p = subprocess.Popen(['pandoc', '-f', 'html', '-t', 'rst'],
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    rst, _ = p.communicate(html_bytes)
    if p.returncode != 0:
        print('Error running pandoc')
    else:
        # Add the title at the top of the output file
        with open(out, 'wb') as f:
            f.write(title + '\n')
            f.write(('~' * len(title)) + '\n\n')
            f.write(rst)
        print('Wrote {}'.format(out))


if __name__ == '__main__':
    main()
