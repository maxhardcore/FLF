# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 21:54:37 2021

@author: Linus
"""
import re
import requests
import base64
from selenium import webdriver
from bs4 import BeautifulSoup

browser = webdriver.Firefox()
searchWord = "tortilla"
sW = "asdasnfb"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}
def GetAudio(searchWord):
    
    mp3url = "https://forvo.com/mp3/"
    wordurl = "https://forvo.com/word/" + searchWord + "/#es/"
    response = requests.get(wordurl, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    htmlSource = str(soup.find_all("div", {"id": "language-container-es"}))
    correctPartOfHtml = re.compile(r'(?<=Play)(.*?)(?=\'\,\')').findall(htmlSource)
    encryptedLinks = [','.join(x.split('\'')[1:]) for x in correctPartOfHtml]
    decryptedLinks = [base64.b64decode(x).decode() for x in encryptedLinks]
    if decryptedLinks:
        browser.get(mp3url + decryptedLinks[0])
        
        
GetAudio("tortilla")
print("lul")