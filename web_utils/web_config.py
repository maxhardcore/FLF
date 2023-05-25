# -*- coding: utf-8 -*-
"""
Created on Thu May  4 23:14:20 2023

@author: Linus
"""
from selenium import webdriver

BROWSER = webdriver.Firefox()
BROWSER.install_addon(r'C:\E\OneDrive\!!!PyProjects\FLF\view_image_context_menu_item-1.3-fx.xpi')
BROWSER.minimize_window()


ALLOWED_FILE_EXTENSIONS = ['jpg', 'png', 'JPG', 'jpeg', 'webp', 'gif', 'svg', 'PNG', 'jfif', 'GIF', 'mp3']

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}

