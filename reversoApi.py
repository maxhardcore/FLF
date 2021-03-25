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


##mit suchwort -> damit ich das suchwort dann unten returnen kann
#beispielsätze?
url = "https://context.reverso.net/traduccion/espanol-ingles/Marco"
# url="https://blog.coinbase.com/"
headers = {'User-Agent': 'Mozilla/5.0'}
response = get(url, headers = headers)
soup = BeautifulSoup(response.text, 'html.parser')
print("lol")

###frequency of translation
##adding a [0] gives only most frequent translation. but one query gives all, so might
#as well return more than just the first? it's a element.ResultSet; can surely iterate.
relevantPartOfHtml1 = soup.find_all("div", {"id": "translations-content"})[0].find_all("a")
for part in relevantPartOfHtml1:
    rofl = re.compile(r'(?<=\>)\w+').findall(part.attrs["title"])[1:]
    print(part.attrs["data-freq"], rofl)
    
relevantPartOfHtml2 = soup.find_all("div", {"class": "src ltr"})
lolek= []
for exampleSentence in relevantPartOfHtml2:
    print((exampleSentence.find_all("span", class_="text")[0]).contents)
    rofl = (exampleSentence.find_all("span", class_="text")[0]).contents
    lolek.append([str(i) for i in rofl])
    
    ##er zeigt alle 20 example sentences an(goil), nicht nur die "non-blocked"
    #zwecks registrierung. nice.
    ##formatieren: erstes element immer (?) \n und whitespaces; zweites = tag (em)
    #gibt es IMMER 3? vor / tag / nach? was wenn satz damit beginnt?
    #nicht drauf verlassen. einfach regexen bzw scannen if in element -> dann regexen
    ##example: Marco -> NICHT immer 3, aber immer multiples of?
    
    ##some contain pronounciation!! check for more cases: noun, conjugated verb, homonyms
    
####SINGLE MOST FREQUENT RESULT
# relevantPartOfHtml = soup.find_all("div", {"id": "translations-content"})[0].find_all("a")[0]
# lol=int(relevantPartOfHtml.attrs["data-freq"])
# print(lol)
# ##translation and type of word
# rofl = relevantPartOfHtml.attrs["title"]
# xd = re.compile(r'(?<=\>)\w+').findall(rofl)[1:]
# print(xd)


##brauche auch sugerencias, suchen nach nomen/verb in zeiten / personen.
##wobei, ist eh lemma was ich kriege.
#verschiedene arten output prüfen, und sehen was ich brauche.
#sorted by frequency, und dann example sentences :---) mit haeufigster uebersetzung

##wort an sich
#hehe = rofl.attrs["title"]
###lookbehind regex! goil!
#re.compile(r'(?<=\>)\w+').findall(hehe)
