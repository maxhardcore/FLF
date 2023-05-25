# -*- coding: utf-8 -*-
"""
Created on Wed May  3 21:26:08 2023

@author: Linus
"""
from shutil import copy


def delete_words(list_of_words, word, file_path):    
    with open(file_path, "r", encoding = "utf-8") as read_file:
        existing_words = read_file.readlines()
    with open(file_path, "w", encoding = "utf-8") as write_file:
        for existing_word in existing_words:
            if existing_word.strip("\n") != word and existing_word:
                write_file.write(f"{existing_word}\n")


def add_lemmata_to_file(lemmata, file_path):
    with open(file_path, "a",encoding="utf-8") as f:
        f.write('\n'.join(lemmata))
        

def backup_file(source_file, backup_file_path):
    copy(f"{source_file}", backup_file_path)
    return(backup_file_path)


def get_searchword_from_file(file_name):
    with open(file_name, "r",encoding="utf-8") as f:
        list_of_words = set(line.strip() for line in f.readlines())
    return(list_of_words)
