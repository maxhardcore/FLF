# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:16:07 2021

@author: Linus
"""



import urllib.request
from tkinter import Tk
from os import path
from selenium import webdriver
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def WaitForCopy(searchterm):
    browser = webdriver.Firefox()
    url = "https://www.reddit.com/r/wow/"
    url = "https://www.google.com/search?q=perro&client=firefox-b-d&hl=de&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiOwJzJpOzvAhUPCuwKHYJlB-QQ_AUoAnoECAEQBA&biw=1920&bih=1005"
    url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1920&bih=1020&q={searchterm}"
    browser.get(url)
    location = r'C:\Users\Linus\Desktop'
    filename = searchterm + '.jpg'
    imageUrlCopied = False
    fileExtensions = ['jpg', 'png', 'JPG', 'jpeg', 'webp', 'gif', 'svg', 'PNG', 'jfif', 'GIF', 'mp3']
    while imageUrlCopied == False:
        WebDriverWait(browser, 1000)
        if any(extension in browser.current_url for extension in fileExtensions):
            print(browser.current_url)
            currl = browser.current_url
            joinedurl = path.join(location,filename)
            urllib.request.urlretrieve (currl, joinedurl)
            browser.quit()
            imageUrlCopied= True
            print(' got it now down')

        
    # if not EC.url_contains('google.com'):
        # # browser.quit()
        # print('nr of windows reached.')


def cbg(location, filename):
    myimage=Tk().clipboard_get()
    joinedurl = path.join(location,filename)
    urllib.request.urlretrieve (myimage, joinedurl)
    print('file successfully saved')
    
    

    
lokation = r'C:\Users\Linus\Desktop'
# cbg(lokation, 'lphrules.jpg')
WaitForCopy('schlurl')



#https://stackoverflow.com/questions/37906534/how-to-wait-for-a-specific-manual-action-using-selenium-python
