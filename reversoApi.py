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
                'skipped the word, do something'
            else:
                pickedAll = True
                'picked all translations, did not skip'
        else:
            translation = LemmaTypeFreq[int(chosenTranslation)][0][0]
            pickedTranslations.append(translation)
    return pickedTranslations

def GetExampleSentence(searchWord, pickedWords):
    headers = {'User-Agent': 'Mozilla/5.0'}
    formattedSentences = []
    browser = webdriver.Firefox()
    
    for translation in pickedWords:
        url = r"https://context.reverso.net/traduccion/espanol-ingles/" + searchWord + '#' + translation
        browser = webdriver.Firefox()
        browser.get(url)
        print(browser.current_url)
        
        
        
        
        rawSentences= []
        rawSentencesTrl = []
        ####################
        ##with BeautifulSoup:############
        ###################
        # response = get(url, headers = headers)
        ##original example sentences
        # relevantPartOfHtml2 = soup.find_all("div", {"class": "src ltr"})
        # for exampleSentence in relevantPartOfHtml2:
            # rawHtml = (exampleSentence.find_all("span", class_="text")[0]).contents
            # rawSentences.append([str(i) for i in rawHtml])
        ##Translated example sentences
        # relevantPartOfHtml3 = soup.find_all("div", {"class": "trg ltr"})
        # for exampleSentenceTrl in relevantPartOfHtml3:
            # rawHtmlTrl = (exampleSentenceTrl.find_all("span", class_="text")[0]).contents
            # rawSentencesTrl.append([str(i) for i in rawHtmlTrl])
        ###FORMATTING
            #remove the line breaks and unnecessary whitespaces
        # for nonFormattedSentence in rawSentences:
        #     if nonFormattedSentence[0] == '\n':
        #         del nonFormattedSentence[0]
        #     else:
        #         nonFormattedSentence[0] = nonFormattedSentence[0][11:]
    
            #concatenate into a single string
            # stringParts = ''
            # for parts in nonFormattedSentence:
            #     stringParts += str(parts)
            # print(stringParts, ' conc')
            #replace <em> (cursive) with <strong> (bold)
            # firstEmReplaced = re.sub('<em>', '<strong>', stringParts)
            # formattedSentence = re.sub('</em>', '</strong>', firstEmReplaced)
            # print(formattedSentence, ' strong')
            # formattedSentences.append(formattedSentence)
        
        ##original example sentences

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
    

        # re.sub(pickedWord, '<strong>' + pickedWord + '</strong>', exampleSentence.text)
            
        browser.quit()

    return (rawSentences, rawSentencesTrl)

#https://context.reverso.net/traduccion/ingles-aleman/concatenate#verkn%C3%BCpfen
#https://context.reverso.net/traduccion/ingles-aleman/concatenate#verketten
##also suburl mit #beispielwort -> daraus die sätze getten. neue soup nach auswahl der übersetzung -> bsp sätze get.

y = FrequencyOfTranslation()
w = PickTranslations(y)
z= GetExampleSentence(searchWord, w)
print('sufi')     
    
    



##brauche auch sugerencias, suchen nach nomen/verb in zeiten / personen.
##wobei, ist eh lemma was ich kriege.
