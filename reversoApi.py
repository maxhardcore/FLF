# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 20:26:05 2021

@author: Linus
"""

from bs4 import BeautifulSoup
from requests import get
import re
#https://github.com/kerrickstaley/genanki
#https://python.plainenglish.io/make-flashier-flashcards-automating-anki-with-python-2744ed025366
#https://pypi.org/project/ankipandas/
#https://android.stackexchange.com/questions/87167/how-do-you-merge-decks-in-anki
#https://pypi.org/project/Reverso-API/

# from reverso_context_api import Client
# import itertools

# client = Client("es", "de")


# x = list(itertools.islice(client.get_translation_samples("azar", cleanup=False), 3))

# print("lol")
# for context in client.get_translation_samples("quiere", cleanup=True):
#     print(context)


url = "https://context.reverso.net/traduccion/espanol-ingles/vender"
# url="https://blog.coinbase.com/"
headers = {'User-Agent': 'Mozilla/5.0'}
response = get(url, headers = headers)
soup = BeautifulSoup(response.text, 'html.parser')
print("lol")

###Häufigkeit der Uebersetzung:
# lol=soup.find_all("div", {"id": "translations-content"})[0]
#rofl = lol.find_all("a"([0])
#rofl.attrs["data-freq"]

##brauche auch sugerencias, suchen nach nomen/verb in zeiten / personen.
#verschiedene arten output prüfen, und sehen was ich brauche.
#sorted by frequency, und dann example sentences :---) mit haeufigster uebersetzung

##wort an sich
#hehe = rofl.attrs["title"]
###lookbehind regex! goil!
#re.compile(r'(?<=\>)\w+').findall(hehe)
