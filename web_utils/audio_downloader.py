# -*- coding: utf-8 -*-
"""
Created on Wed May  3 21:22:23 2023

@author: Linus
"""
from base64 import b64decode
from vlc import MediaPlayer


def get_encrypted_audio_url(audio_soup, headers):
    try:
        encrypted_audio_url = audio_soup.select_one("div[id*=play_]").attrs["onclick"] #where '*=' is 'contains'
    except (TypeError, AttributeError):
        return
    return encrypted_audio_url


def decrypt_audio_url(encrypted_url):
    if encrypted_url is None:
        return
    encrypted_link_suffix = encrypted_url.split(",\'")[1][:-1]
    decrypted_link_suffix = b64decode(encrypted_link_suffix).decode()
    MediaPlayer("https://forvo.com/mp3/" + decrypted_link_suffix).play()
    
    return "https://forvo.com/mp3/" + decrypted_link_suffix
