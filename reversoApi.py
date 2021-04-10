# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 20:26:05 2021

@author: Linus
"""

from bs4 import BeautifulSoup
from requests import get
import re
import time
from docx import Document
#https://github.com/kerrickstaley/genanki
#https://python.plainenglish.io/make-flashier-flashcards-automating-anki-with-python-2744ed025366
#https://pypi.org/project/ankipandas/
#https://android.stackexchange.com/questions/87167/how-do-you-merge-decks-in-anki
#https://pypi.org/project/Reverso-API/



##mit suchwort -> damit ich das suchwort dann unten returnen kann
#beispielsätze?
url = "https://context.reverso.net/traduccion/espanol-ingles/leña"
headers = {'User-Agent': 'Mozilla/5.0'}
response = get(url, headers = headers)
soup = BeautifulSoup(response.text, 'html.parser')


def FrequencyOfTranslation():
    relevantPartOfHtml1 = soup.find_all("div", {"id": "translations-content"})[0].find_all("a")
    
    LemmaTypeFreq = []
    for part in relevantPartOfHtml1:
         ##get Lemma,
        lemma = re.compile(r'(?<=\'translation\'\>)(.*?)(?=\<\/em\>)').findall(part.attrs["title"])
        if len(re.compile(r'(?<=\>)\w+').findall(part.attrs["title"])) >2:
        ##(if exists:) Type  (also sometimes contains pronounciation IPA)
            typeList = re.compile(r'(?<=\>)\w+').findall(part.attrs["title"])[2:]
        else:
            typeList = []
        ##Frequency
        frequency = int(part.attrs["data-freq"])
        LemmaTypeFreq.append([lemma, typeList, frequency])
    ##STOPS IF WORD CONTAINS '-', needs fixing!
    print('lol')
    return LemmaTypeFreq

def PickWord(LemmaTypeFreq):
    for i in range(len(LemmaTypeFreq)):
        print(str(i), ':', LemmaTypeFreq[i])
    #user picks from all offered translations, then presses Enter to finish.
    pickedAll = False
    pickedWords = []
    while pickedAll == False:
        chosenTranslation = (input("Enter choice of translation or press 'Enter' to finish:"))
        if chosenTranslation == "":
            pickedAll = True
        else:
            pickedWord = LemmaTypeFreq[int(chosenTranslation)][0][0]
            pickedWords.append(pickedWord)
    return pickedWords

def GetExampleSentence(pickedWords):
    headers = {'User-Agent': 'Mozilla/5.0'}
    formattedSentences = []
    
    for pickedWord in pickedWords:
        url = r"https://context.reverso.net/traduccion/espanol-ingles/leña" + '#' + pickedWord
        
        response = get(url, headers = headers)
        print(response.url)
        
        ####show current url, wait 15 sec, show current url.
        soup = BeautifulSoup(response.text, 'html.parser')
        f = open(pickedWord + ".txt", "a", encoding='utf-8')
        f.write(str(soup))
        f.close()
        
        
        rawSentences= []
        rawSentencesTrl = []
        
        ##original example sentences
        relevantPartOfHtml2 = soup.find_all("div", {"class": "src ltr"})
        for exampleSentence in relevantPartOfHtml2:
            # print((exampleSentence.find_all("span", class_="text")[0]).contents)
            rawHtml = (exampleSentence.find_all("span", class_="text")[0]).contents
            rawSentences.append([str(i) for i in rawHtml])
        
        ##Translated example sentences
        relevantPartOfHtml3 = soup.find_all("div", {"class": "trg ltr"})
        for exampleSentenceTrl in relevantPartOfHtml3:
            # print((exampleSentence.find_all("span", class_="text")[0]).contents)
            rawHtmlTrl = (exampleSentenceTrl.find_all("span", class_="text")[0]).contents
            rawSentencesTrl.append([str(i) for i in rawHtmlTrl])
        
    
        ###FORMATTING
            #remove the line breaks and unnecessary whitespaces
        for nonFormattedSentence in rawSentences:
            if nonFormattedSentence[0] == '\n':
                del nonFormattedSentence[0]
            else:
                nonFormattedSentence[0] = nonFormattedSentence[0][11:]
    
            #concatenate into a single string
            stringParts = ''
            for parts in nonFormattedSentence:
                stringParts += str(parts)
            print(stringParts, ' conc')
            #replace <em> (cursive) with <strong> (bold)
            firstEmReplaced = re.sub('<em>', '<strong>', stringParts)
            formattedSentence = re.sub('</em>', '</strong>', firstEmReplaced)
            print(formattedSentence, ' strong')
            formattedSentences.append(formattedSentence)

    return formattedSentences

#https://context.reverso.net/traduccion/ingles-aleman/concatenate#verkn%C3%BCpfen
#https://context.reverso.net/traduccion/ingles-aleman/concatenate#verketten
##also suburl mit #beispielwort -> daraus die sätze getten. neue soup nach auswahl der übersetzung -> bsp sätze get.

y = FrequencyOfTranslation()
w = PickWord(y)
z= GetExampleSentence(w)
print('sufi')     
    
    ##example sentences für ausgewählte übersetzung anzeigen!
    ##doch händisch auswählen? was spare ich dann. reverso eingeben, kopieren, pic suchen,
    #pic speichern, flashcard erstellen. habe aber noch immer die connection mit
    #pic und auswahl des wortes / satzes.
    
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
FrequencyOfTranslation()