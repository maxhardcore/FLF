# -*- coding: utf-8 -*-
"""
Created on Wed May  3 21:20:00 2023

@author: Linus
"""

import urllib.request            
from selenium.webdriver.support.ui import WebDriverWait   
from time import sleep        


def download_image(searchterm, search_language, browser, anki_media_folder, allowed_file_extensions, unique_image_name):
    
    google_search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1920&bih=1020&q={searchterm} {search_language}"
    browser.get(google_search_url) 
    browser.maximize_window()
    
    image_path = ""
    while not image_path:
        WebDriverWait(browser, 1000)
        #as soon as url contains a link to an image
        if any(extension in browser.current_url for extension in allowed_file_extensions):
            current_url = browser.current_url
            try:
                urllib.request.urlretrieve(current_url, unique_image_name)
            except:
                print('pick another image')
                browser.minimize_window()
                sleep(10)
                continue                    
            else:
                print(' got it now down')
                unique_path = unique_image_name[unique_image_name.rindex('\\')+1:]
                image_path = f"<img src={unique_path}>"

            curr=browser.current_window_handle
            for handle in browser.window_handles:
               browser.switch_to.window(handle)
               if handle != curr:
                  browser.close()
            try:      
                browser.minimize_window()
            except:
                print ('NoSuchWindowException')
    return image_path


# xabc = download_image("vender", browser)