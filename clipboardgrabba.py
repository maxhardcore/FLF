# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:16:07 2021

@author: Linus
"""



import urllib.request
from tkinter import Tk
from os import path

def cbg(location, filename):
    myimage=Tk().clipboard_get()
    joinedurl = path.join(location,filename)
    urllib.request.urlretrieve (myimage, joinedurl)
    print('file successfully saved')
    
lokation = r'C:\Users\Linus\Desktop'
cbg(lokation, 'lphrules.jpg')