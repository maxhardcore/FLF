# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 21:54:37 2021

@author: Linus
"""
import re
import requests
import json
import base64
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request 

browser = webdriver.Firefox()

#https://github.com/RyanSu98/forvo_api_free/blob/master/en.py

searchWord = "tortilla"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}
    
mp3url = "https://forvo.com/mp3/"
wordurl = "https://forvo.com/word/" + searchWord + "/#es/"
response = requests.get(wordurl, headers = headers)
# browser.get(wordurl)
soup = BeautifulSoup(response.text, 'html.parser')
# html_source = browser.page_source


possibleLemmas = str(soup.find_all("div", {"id": "language-container-es"}))

# (?<=\,\')(.*?)(\'\,\')
#  https://www.base64decode.org/
#  https://forvo.com/mp3/9023874/41/9023874_41_964_289985.mp3

#(?<=Play\(\d*\,\')(.*?)(?=\'\,\')


def LinkGrabber(nl):
    pickedAll = False
    pickedTranslations = []
    pickedNumbers=[]
    chosenTranslation = (input("Enter choice of translation or press 'Enter' to finish:"))
    if chosenTranslation =="":
        if not pickedTranslations:
            pickedAll = True
            # print('deleting picktrl', searchWord)
            return pickedTranslations
        else:
            pickedAll = True
    else: # if input is not 'enter'

        if int(chosenTranslation) not in pickedNumbers:
            if chosenTranslation.isdigit() and int(chosenTranslation) < len(nl):
                        translation = "https://forvo.com/mp3/" + nl[int(chosenTranslation)]
                        pickedTranslations.append(translation)
                        pickedNumbers.append(int(chosenTranslation))  
    return pickedTranslations


correctSearchWord = re.compile(r'(?<=Play)(.*?)(?=\'\,\')').findall(possibleLemmas)
new_str = [','.join(x.split('\'')[1:]) for x in correctSearchWord]
nl = [base64.b64decode(x).decode() for x in new_str]
a = LinkGrabber(nl)


# url = 'http://google.com/favicon.ico'
# r = requests.get(url, allow_redirects=True)
# open('google.ico', 'wb').write(r.content)
print("lul")