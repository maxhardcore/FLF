# -*- coding: utf-8 -*-
"""
Created on Thu May  4 23:16:58 2023

@author: Linus
"""

from bs4 import BeautifulSoup
from requests import get, utils

HEADERS = utils.default_headers()
HEADERS.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

DICTIONARY_URL = "https://context.reverso.net/traduccion/"
LANGUAGE_PAIR = "espanol-ingles/"
SEARCH_WORD = "agredido"

url =  f"{DICTIONARY_URL}{LANGUAGE_PAIR}{SEARCH_WORD}"
page = get(url, headers = HEADERS)
soup = BeautifulSoup(page.content, "html.parser")