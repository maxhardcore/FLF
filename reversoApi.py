# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 20:26:05 2021

@author: Linus
"""

from bs4 import BeautifulSoup
from requests import get
import re
import time
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
import clipboardgrabba
#https://github.com/kerrickstaley/genanki
#https://python.plainenglish.io/make-flashier-flashcards-automating-anki-with-python-2744ed025366
#https://pypi.org/project/ankipandas/
#https://android.stackexchange.com/questions/87167/how-do-you-merge-decks-in-anki
#https://pypi.org/project/Reverso-API/



##mit suchwort -> damit ich das suchwort dann unten returnen kann
#beispielsätze?


def GetPossibleLemmas(soup, searchWord, file):
    pickedLemma = False
    pickedLemmas = []
    pickedNumbers = []
    
    print('-----possible lemmas-----')
    try:
        possibleLemmas = soup.find_all("div", {"class": "notice suggested search"})[0].find_all("a")
    except IndexError:
        possibleLemmas = []
        print(searchWord, 'is the only valid lemma')

    if possibleLemmas:
        i=0
        for lemma in possibleLemmas:
            print(i, lemma.text)
            i+=1
        
        while pickedLemma == False:
            chosenLemma = (input("Enter choice of lemma or press 'Enter' to finish:"))
            if chosenLemma == "":
                #if nothing has been picked and user presses Enter
                if not pickedLemmas:
                    pickedLemma = True
                    DelWords(file, searchWord)
                    print('deleting', searchWord)
                else: # if some options have already been picked and then Enter is pressed
                    pickedLemma = True
                    
                    print('picked all lemmas, did not skip')
            else: # if input is not 'enter'
                if int(chosenLemma) not in pickedNumbers:
                    if chosenLemma.isdigit() and int(chosenLemma) < len(possibleLemmas):

                        ##appenden zum DocFile
                        pickedNumbers.append(int(chosenLemma))
                        pickedLemmas.append(possibleLemmas[int(chosenLemma)].text)
                    else: #if input is too high or not an integer
                        print('Please enter a valid integer only')
                else: #if chosen Number already in picked Numbers
                    print('already chose this translation, please make a different choice') 
        print(pickedLemmas)
        AddLemmasToTextFile(pickedLemmas, file)
        
def DelWords(file, deleteThisWord):
    with open(file, "r") as f:
        lines = f.readlines()
    # addedWords = [v[0] for n in noteArray for v in n]
    with open(file, "w") as f:
        for line in lines:
            #only writes those that are not yet added, thus eliminates added words.
            if line.strip("\n") != deleteThisWord:
                if line.strip("\n") != "":
                    f.write(line)
                # print('deleted word ', line.strip("\n"))

def AddLemmasToTextFile(pickedLemmas, file):
    with open(file, "r") as f:
        lines = f.readlines()
    strippedLines = [line.strip() for line in lines]   
    with open(file, "a") as f:
        f.write('\n')
        for lemma in pickedLemmas:
            if lemma not in strippedLines:
        #only writes those that are not yet added, thus eliminates added words.
                f.write(lemma+'\n')
                print('added', lemma, 'to file')
    
def CountNonexisting():
    global nonexisting
    nonexisting += 1
    return nonexisting

def FrequencyOfTranslation(searchWord, file):
    
    
    # for searchWord in searchList:
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://context.reverso.net/traduccion/espanol-aleman/" + searchWord
    response = get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    LemmaTypeFreq = []
    
    ##if misspelling, delete searchWord from txt, and add correct spelling at the end.
    try:
        relevantPartOfHtml0 = soup.find_all("div", {"class": "notice applied pair"})
        correctSpelling = relevantPartOfHtml0[0].find_all("span")[0]["title"]
        correctSearchWord = re.compile(r'(?<=\")(.*?)(?=\")').findall(correctSpelling)[0]
        AddLemmasToTextFile([correctSearchWord], file)
        DelWords(file, searchWord)
        print(searchWord, " corrected to ", correctSearchWord)
        return LemmaTypeFreq
    except: #when the word is spelt correctly, dont do anything. 
        print(searchWord, "was the correct spelling")
    
    try:
        relevantPartOfHtml1 = soup.find_all("div", {"id": "translations-content"})[0].find_all("a")
    except IndexError:
        print('no results found for FoT', searchWord)
        CountNonexisting()
        return LemmaTypeFreq
    
    
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
    print('-----', searchWord, '-----')
    ##Give user option to lemmatize
    GetPossibleLemmas(soup, searchWord, file)
    
    return LemmaTypeFreq

def PickTranslations(searchWord, file):
    LemmaTypeFreq = FrequencyOfTranslation(searchWord, file)
    pickedAll = False
    pickedTranslations = []
    pickedNumbers = []
    if LemmaTypeFreq:  
        for i in range(len(LemmaTypeFreq)):
            print(str(i), ':', LemmaTypeFreq[i])
        print('-----', searchWord, '-----')
    else:
    #     print('well there was no result, so no PickTransl')
        print(' no translation found for ', searchWord, ' deleting')
        DelWords(file, searchWord)
        return pickedTranslations
    #user picks from all offered translations, then presses Enter to finish.

    while pickedAll == False:
        if len(LemmaTypeFreq) == 1:
            pickedTranslation = LemmaTypeFreq[0][0]
            print('-there was only one option')
            return pickedTranslation
        elif len(pickedTranslations) == len(LemmaTypeFreq):
            print('-no more choice-')
            return pickedTranslations
        chosenTranslation = (input("Enter choice of translation or press 'Enter' to finish:"))
        if chosenTranslation == "":
            #if nothing has been picked and user presses Enter
            if not pickedTranslations:
                pickedAll = True
                DelWords(file, searchWord)
                print('deleting picktrl', searchWord)
                return pickedTranslations
            else:
                pickedAll = True
                print('picked all translations, did not skip')
        else: # if input is not 'enter'
            if int(chosenTranslation) not in pickedNumbers:
                if chosenTranslation.isdigit() and int(chosenTranslation) < len(LemmaTypeFreq):
                    translation = LemmaTypeFreq[int(chosenTranslation)][0][0]
                    pickedTranslations.append(translation)
                    pickedNumbers.append(int(chosenTranslation))
                else: #if input is too high or not an integer
                    print('Please enter a valid integer only')
            else:
                print('already chose this translation, please make a different choice')
    return pickedTranslations

def GetExampleSentences(searchWord, browser, file):
    pickedWords = PickTranslations(searchWord, file)
    headers = {'User-Agent': 'Mozilla/5.0'}
    formattedSentences = []
    # browser = webdriver.Firefox()
    if pickedWords:
        for translation in pickedWords:
            if translation == "":
                print('did not pick a word')
            else:
                url = r"https://context.reverso.net/traduccion/espanol-aleman/" + searchWord + '#' + translation
                
                browser.get(url)
                time.sleep(3)
                print(browser.current_url)
        
                rawSentences= []
                rawSentencesTrl = []
                rawSentencesCap = []
                rawSentencesCapTrl = []
                #https://stackoverflow.com/questions/57644631/get-the-different-value-from-multiple-elements-with-the-same-class-in-selenium-f
                # print([my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(browser, 105).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "src")))])
                relevantPartOfHtml2 = browser.find_elements_by_class_name("src")
                for exampleSentence in relevantPartOfHtml2:
                    #some src class elements do not contain text. only append those that exist
                    if exampleSentence.text:
                        boldedSentence = re.sub(searchWord, '<strong>' + searchWord + '</strong>', exampleSentence.text)
                        capSentence = re.sub(searchWord, searchWord.upper(), exampleSentence.text)
                        rawSentences.append(boldedSentence)
                        rawSentencesCap.append(capSentence)
                
                relevantPartOfHtml3 = browser.find_elements_by_class_name("trg")
                for exampleSentenceTrl in relevantPartOfHtml3:
                    if exampleSentenceTrl.text:
                        boldedSentenceTrl = re.sub(translation, '<strong>' + translation + '</strong>', exampleSentenceTrl.text)
                        capSentenceTrl = re.sub(translation, translation.upper(), exampleSentenceTrl.text)
                        rawSentencesTrl.append(boldedSentenceTrl)
                        rawSentencesCapTrl.append(capSentenceTrl)
                formattedSentences.append([translation, rawSentences, rawSentencesTrl, rawSentencesCap, rawSentencesCapTrl])
    # else:
    #     print(' GES empty since PickTrans empty')
    # browser.quit()

    return formattedSentences


def PickSentences(searchWord, browser, file):
    pickedSentences = []
    formattedSentences = GetExampleSentences(searchWord, browser, file)
    if formattedSentences:
        for sentences in formattedSentences:
            i=0
            
            for originalSentence in sentences[3]:
                print(i, originalSentence)
                i+=1
            print('------------------------')
            i=0
            for translatedSentence in sentences[4]:
                print(i, translatedSentence)
                i+=1
            
            picked = False
            while picked == False:
                print(searchWord, ':', sentences[0])
                chosenSentence = (input("Enter choice of sentence or press 'Enter' to skip:"))
                if chosenSentence == "":
                    print('deleting the word picksent')
                    DelWords(file, searchWord)
                    picked = True
                    # return pickedSentences
                    continue
                elif chosenSentence.isdigit() and int(chosenSentence) < len(sentences[1]):
                    pic = clipboardgrabba.WaitForCopy(searchWord, sentences[0], browser)
                    pickedSentences.append([searchWord, sentences[0], sentences[1][int(chosenSentence)],sentences[2][int(chosenSentence)], pic])
                    
                    print('did not skip, added')
                    picked = True
                else:
                    print('Please enter a valid integer only')
    # else:
        # print(' no PickSentences since PickTrans empty')
    return pickedSentences





nonexisting = 0


# y = FrequencyOfTranslation('traslado', 'probieren.txt')
# w = PickTranslations(y)
# if w:
#     z= GetExampleSentences(searchWord, w)
# else:
#     print(' did not pick any word')
# a = PickSentences(searchWord, z)
# print('sufi')     
    
    

##https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium

##brauche auch sugerencias, suchen nach nomen/verb in zeiten / personen.
##wobei, ist eh lemma was ich kriege.
