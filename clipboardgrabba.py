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
from urllib.error import HTTPError
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def WaitForCopy(searchterm):
    browser = webdriver.Firefox()
    url = "https://www.reddit.com/r/wow/"
    url = "https://www.google.com/search?q=perro&client=firefox-b-d&hl=de&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiOwJzJpOzvAhUPCuwKHYJlB-QQ_AUoAnoECAEQBA&biw=1920&bih=1005"
    url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1920&bih=1020&q={searchterm}"
    browser.get(url)
    location = r'C:\Users\Linus\Desktop'
    imageUrlCopied = False
    fileExtensions = ['jpg', 'png', 'JPG', 'jpeg', 'webp', 'gif', 'svg', 'PNG', 'jfif', 'GIF', 'mp3']
    while imageUrlCopied == False:
        WebDriverWait(browser, 1000)
        #as soon as url contains a link to an image

        if any(extension in browser.current_url for extension in fileExtensions):
            print(browser.current_url)
            currl = browser.current_url
            
            #check if filename exists already
            i=1
            filePath = CheckUniqueName(location, searchterm + '.jpg')
            # joinedurl = path.join(location,searchterm + '.jpg')
            try:
                urllib.request.urlretrieve (currl, filePath)
            except:
                print('pick another image')
                time.sleep(5)
                continue                    
            else:
                browser.quit()
                imageUrlCopied= True
                print(' got it now down')

        
    # if not EC.url_contains('google.com'):
        # # browser.quit()
        # print('nr of windows reached.')

def CheckUniqueName(location, searchterm):

    base, extension = os.path.splitext(searchterm)
    filePath = os.path.join(location, base + extension)
    if os.path.exists(filePath):
        i=1
        while True:
            newpath = "{0}{2}{1}".format(*path.splitext(filePath) + (i,))
            if os.path.exists(newpath):
                i+=1
            else:
                return(newpath)
    return(filePath)


            


def cbg(location, filename):
    myimage=Tk().clipboard_get()
    joinedurl = path.join(location,filename)
    urllib.request.urlretrieve (myimage, joinedurl)
    print('file successfully saved')
    
    

    
lokation = r'C:\Users\Linus\Desktop'
# cbg(lokation, 'lphrules.jpg')

WaitForCopy('schlurl')
    # except HTTPError:
    #     p)
    
# rofl = CheckUniqueName(lokation, 'schlurl.jpg')
# print(rofl, 'will be the new name')



#https://stackoverflow.com/questions/37906534/how-to-wait-for-a-specific-manual-action-using-selenium-python
