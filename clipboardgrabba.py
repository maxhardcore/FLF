# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:16:07 2021

@author: Linus
"""



import urllib.request

from os import path
import os
import time
from selenium.webdriver.support.ui import WebDriverWait




def WaitForCopy(searchterm, translation, browser):
    # urlSearchterm = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1920&bih=1020&q={searchterm}"
    urlSearchtermEsp = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1920&bih=1020&q={searchterm} español"
    # urlTranslate = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1920&bih=1020&q={translation}"
    
    browser.get(urlSearchtermEsp) 
        
    
    
    
    browser.maximize_window()
    
    location = r'C:\Users\Linus\AppData\Roaming\Anki2\User 1\collection.media'
    imageUrlCopied = False
    fileExtensions = ['jpg', 'png', 'JPG', 'jpeg', 'webp', 'gif', 'svg', 'PNG', 'jfif', 'GIF', 'mp3']
    while imageUrlCopied == False:
        WebDriverWait(browser, 1000)
        #as soon as url contains a link to an image
        if any(extension in browser.current_url for extension in fileExtensions):
            currl = browser.current_url
            
            #check if filename exists already
            filePath = CheckUniqueName(location, searchterm + '.jpg')
            try:
                urllib.request.urlretrieve (currl, filePath[0])
            except:
                print('pick another image')
                browser.minimize_window()
                time.sleep(10)
                continue                    
            else:
                imageUrlCopied= True
                print(' got it now down')
                imagePath = '<img src="{0}.jpg">'.format(searchterm + filePath[1])

            curr=browser.current_window_handle
            for handle in browser.window_handles:
               browser.switch_to.window(handle)
               if handle != curr:
                  browser.close()
            try:      
                browser.minimize_window()
            except:
                print ('NoSuchWindowException')
    return imagePath

        
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
                return(newpath, str(i))
    else:
        i=''
    return(filePath, str(i))
    
lokation = r'C:\Users\Linus\AppData\Roaming\Anki2\User 1\collection.media'
