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
from selenium import webdriver
#https://github.com/kerrickstaley/genanki
#https://python.plainenglish.io/make-flashier-flashcards-automating-anki-with-python-2744ed025366
#https://pypi.org/project/ankipandas/
#https://android.stackexchange.com/questions/87167/how-do-you-merge-decks-in-anki
#https://pypi.org/project/Reverso-API/



##mit suchwort -> damit ich das suchwort dann unten returnen kann
#beispielsätze?
searchWord = 'leña'
url = "https://context.reverso.net/traduccion/espanol-ingles/" + searchWord
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

def PickTranslations(LemmaTypeFreq):
    for i in range(len(LemmaTypeFreq)):
        print(str(i), ':', LemmaTypeFreq[i])
    #user picks from all offered translations, then presses Enter to finish.
    pickedAll = False
    pickedTranslations = []
    while pickedAll == False:
        chosenTranslation = (input("Enter choice of translation or press 'Enter' to finish:"))
        if chosenTranslation == "":
            if not pickedTranslations:
                pickedAll = True
                print('skipped the word, do something')
            else:
                pickedAll = True
                print('picked all translations, did not skip')
        else:
            if chosenTranslation.isdigit() and int(chosenTranslation) < len(LemmaTypeFreq):
                translation = LemmaTypeFreq[int(chosenTranslation)][0][0]
                pickedTranslations.append(translation)
            else:
                print('Please enter an Integer only')
    return pickedTranslations

def GetExampleSentences(searchWord, pickedWords):
    headers = {'User-Agent': 'Mozilla/5.0'}
    formattedSentences = []
    
    for translation in pickedWords:
        url = r"https://context.reverso.net/traduccion/espanol-ingles/" + searchWord + '#' + translation
        browser = webdriver.Firefox()
        browser.get(url)
        print(browser.current_url)
        rawSentences= []
        rawSentencesTrl = []
        relevantPartOfHtml2 = browser.find_elements_by_class_name("src")
        
        for exampleSentence in relevantPartOfHtml2:
            #some src class elements do not contain text. only append those that exist
            if exampleSentence.text:
                boldedSentence = re.sub(searchWord, '<strong>' + searchWord + '</strong>', exampleSentence.text)
                rawSentences.append(boldedSentence)
        
        relevantPartOfHtml3 = browser.find_elements_by_class_name("trg")
        for exampleSentenceTrl in relevantPartOfHtml3:
            if exampleSentenceTrl.text:
                rawSentencesTrl.append(exampleSentenceTrl.text)
                
        browser.quit()

    return (rawSentences, rawSentencesTrl)




y = FrequencyOfTranslation()
w = PickTranslations(y)
if w:
    z= GetExampleSentences(searchWord, w)
else:
    print(' did not pick any word')
print('sufi')     
    
    



##brauche auch sugerencias, suchen nach nomen/verb in zeiten / personen.
##wobei, ist eh lemma was ich kriege.
