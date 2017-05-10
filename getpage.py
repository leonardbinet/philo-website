#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import logging
from urllib.parse import urldefrag, unquote
import setpath
from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
from werkzeug.contrib.cache import SimpleCache

# Si vous écrivez des fonctions en plus, faites-le ici


def getJSON(page):
    params = urlencode({
        'format': 'json',
        'action': 'parse',
        'prop': 'text',
        'redirects': 'true',
        'page': page})
    API = "https://fr.wikipedia.org/w/api.php"
    response = urlopen(API + "?" + params)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']
        content = parsed['parse']['text']['*']
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page):
    assert isinstance(page, str)

    urls = []
    cache = SimpleCache()
    cached_object = cache.get(page)
    if cached_object is not None:
        logging.info("Using cached result for page %s." % page)
        title, urls = cached_object
        return title, urls

    logging.info("Page %s not found in cache" % page)
    title, content = getRawPage(page)
    if title:
        title = urldefrag(unquote(title))[0]
        title = title.replace("_", " ")

    if not content:
        cache.set(page, (title, None), timeout=5 * 60)
        return title, None

    soup = BeautifulSoup(content, 'html.parser')
    for paragraph in soup.find_all('p', recursive=False):
        for link in paragraph.find_all('a'):
            url = link.get('href')
            if url.startswith("/wiki/"):
                url = url[6:]
                url = unquote(url)
                urls.append(url)

    urls = list(set(urls))
    urls = urls[:10]
    cache.set(page, (title, urls), timeout=5 * 60)

    return title, urls

if __name__ == '__main__':
    pass

    # print(getJSON("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Histoire"))
