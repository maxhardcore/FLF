# -*- coding: utf-8 -*-
"""
Created on Wed May  3 21:51:08 2023

@author: Linus
"""
from urllib.parse import unquote



def get_lemmas(soup):
    lemmata = [lemma.text for lemma in soup.findAll("a", {"class": "dym-link"})]
    return lemmata 

    
def get_word_frequency(soup):
    frequency_and_translation = [[x.get("data-freq"), x.get("data-term")] for x in soup.find_all('a', {"data-freq": True})] 
    return frequency_and_translation


def get_phrases(soup):
    example_phrases = [sentence.text.strip() for sentence in soup.findAll("div", {"class": ["trg ltr", "src ltr"]})]
    it = iter(example_phrases)  # turns a list into an iterable
    example_phrase_tuple_list = list(zip(it, it)) # makes tuples of 2 elements of the list
    return example_phrase_tuple_list


def rectify_typos(page, search_word):
    if search_word in unquote(page.url):
        pass
    else:
        return page.url[page.url.rindex('/')+1:]
