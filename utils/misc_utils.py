# -*- coding: utf-8 -*-
"""
Created on Wed May  3 21:55:39 2023

@author: Linus
"""
from os import path
from re import search, sub, IGNORECASE

def choose_from_list(list_of_options, maximum_choices):
    for o, t in enumerate(list_of_options):
        print(o,t)
    choices = []
    if len(list_of_options) == 1:
        print("Only one option!")
        return list_of_options
    while len(choices) < maximum_choices:
        user_input = input("Please choose: ")
        if user_input == "":
            break
        elif not user_input.isdigit() or not 0 <= int(user_input) < len(list_of_options):
            print("Please input a valid integer. ")
            continue
        else:
            choices.append(int(user_input))
            print(f"Selected: {choices}")

    print("All chosen or list full!")
    return [list_of_options[choice] for choice in choices]


def check_unique_name(location, search_word, file_extension):
    if path.isfile(search_word):
        search_word = path.splitext(path.basename(search_word))[0]
    file_path = path.join(location, search_word)
    if not path.exists(f"{file_path}.{file_extension}"):
        return(f"{file_path}.{file_extension}") #exits out early if unique without numbers
    
    i = 1
    while path.exists(f"{file_path}_{i}.{file_extension}"): 
        i += 1
    return(f"{file_path}_{i}.{file_extension}") # returns uniquely incremented file_path


def bold_word_in_phrase(search_word, phrase):
    case_insensitive_word = search(search_word, phrase, flags = IGNORECASE).group()
    return sub(case_insensitive_word, f"<strong>{case_insensitive_word}</strong>", phrase, flags=IGNORECASE)

