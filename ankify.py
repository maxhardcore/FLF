# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 22:10:32 2023

@author: Linus
"""    
#-----------------------
from utils import misc_utils, config
from file_utils import sourcefile_modifier
from web_utils import audio_downloader, image_downloader, web_config, web_dict_crawler
from anki_utils import card_utils

import requests
from bs4 import BeautifulSoup


##Configuration:
###File Section
SOURCE_FILE = r'C:\E\OneDrive\!!!PyProjects\FLF\nonreflex_utf8.txt'
BACKUP_FOLDER = r'C:\E\OneDrive\!!!PyProjects\FLF\backup'


###Web Section
##phrases
DICTIONARY_URL = r"https://context.reverso.net/traduccion/"
LANGUAGE = r"espanol-aleman/"
##audio
AUDIO_URL = r'https://forvo.com/word/'
AUDIO_LANGUAGE = r'/#es/'
##images
SEARCH_LANGUAGE = r'español'

###Anki Section
ANKI_COLLECTION_PATH = r'C:\Users\Linus\AppData\Roaming\Anki2\User 1\collection.anki2'
ANKI_MEDIA_PATH = r"C:\Users\Linus\AppData\Roaming\Anki2\User 1\collection.media\\"
ANKI_DECK_NAME = 'Espanol' # or "Lisaan Masri"
ANKI_MODEL_NAME = "2. Picture Words" # or "Arabic""


##alles in web_dict_crawler

NON_EXISTING_WORDS = 0
CARD_COUNTER = 0
WORD_COUNTER = 0

list_of_words = sourcefile_modifier.get_searchword_from_file(SOURCE_FILE)

if __name__ == '__main__':
    latest_backup_file_name = misc_utils.check_unique_name(BACKUP_FOLDER,SOURCE_FILE,"txt")    
    print(sourcefile_modifier.backup_file(SOURCE_FILE, latest_backup_file_name))
    try:
        for word in list_of_words:
            print(f"----{word}-----")
            WORD_COUNTER += 1
            page = requests.get(f"{DICTIONARY_URL}{LANGUAGE}{word}", headers = web_config.HEADERS)
            soup = BeautifulSoup(page.content, "html.parser")
            if web_dict_crawler.rectify_typos(page, word):
                sourcefile_modifier.add_lemmata_to_file(web_dict_crawler.rectify_typos(page, word), SOURCE_FILE)
                sourcefile_modifier.delete_words(list_of_words, word, SOURCE_FILE)
                continue
            
            audio_url = f'{AUDIO_URL}{word}{AUDIO_LANGUAGE}'
            audio_response = requests.get(audio_url, headers = web_config.HEADERS)
            audio_soup = BeautifulSoup(audio_response.text, 'html.parser')
            anki_audio = audio_downloader.decrypt_audio_url(audio_downloader.get_encrypted_audio_url(audio_soup, web_config.HEADERS))

            sourcefile_modifier.add_lemmata_to_file(misc_utils.choose_from_list(web_dict_crawler.get_lemmas(soup),99), SOURCE_FILE)
            for selected_word in misc_utils.choose_from_list(web_dict_crawler.get_word_frequency(soup), 99):
                selected_page = requests.get(f"{DICTIONARY_URL}{LANGUAGE}{word}#{selected_word[1]}", headers = web_config.HEADERS)
                selected_soup = BeautifulSoup(selected_page.content, "html.parser")
                selected_phrases = misc_utils.choose_from_list(web_dict_crawler.get_phrases(selected_soup), 1)
                ##also, bold it in all phrases / highlight it
                ##do if statements to I skip all possible (check my previous)
                if selected_phrases:
                    unique_image_name = misc_utils.check_unique_name(ANKI_MEDIA_PATH, word, 'jpg')
                    anki_image = image_downloader.download_image(word, SEARCH_LANGUAGE, web_config.BROWSER, ANKI_MEDIA_PATH, web_config.ALLOWED_FILE_EXTENSIONS, unique_image_name)
                    anki_phrase = misc_utils.bold_word_in_phrase(word, selected_phrases[0][0])
                    card_utils.create_card(anki_image, anki_phrase, anki_audio, ANKI_COLLECTION_PATH, ANKI_MODEL_NAME, ANKI_DECK_NAME)
                    CARD_COUNTER += 1
            sourcefile_modifier.delete_words(list_of_words, word, SOURCE_FILE)
            print(f"{WORD_COUNTER} gone through - {CARD_COUNTER} cards created")
    except KeyboardInterrupt:
        pass
    print(f"{len(list_of_words)} words remaining")
    web_config.BROWSER.quit()
    
    
    ##the problem is the javascript shit - maybe find a different approach this time
    #for now: print only those phrases that contain the selected_word[1]
    ##but make a branch before that. try not to use selenium tbh
    

   
    ##can I rewrite some stuff into a function and decrease length? like setup everything elsewhere
    ##or somehow catch edge cases and exit quicker (happy path)?
    ##download audio, make own folder for each language in collection, also for media
    ##u will get 1 gamu!
    ##make same or bettter - more modifiable (nothing hardcoded, all setup in one file)
    ##target anki deck correctly - still doesn't work!, worked when I did it manually. wonder why
    ##try /w arabic - what needs changing (but only after all works flawlessly)
    
    ##configparser -> read all from one file, es, arabic,...etc.
    

    
##if I skip phrase -> don't download image

    
    #nschlanki:
        #pic: f'<img src="{unique_image_name}.jpg">'
        #phrase: selected_phrases[0][1]
        #nschlaudio: if nschlaudio: nschlaudio
        
##TODO: conn err from frequency_of_translation reverso_Api (connection issue handling)
##TODO: make a GIT branch
##TODO: try /w config file -> new branch
##TODO: try /w arabic
##TODO: config file
##TODO: adapt create_card to multiple fields / flexible
##TODO: then see how I can minimize calls to similar functions / objects
##TODO: all functions onyl get the param they need and do only one thing
##TODO: param and result typing
##TODO: needs if clauses so it doesn't break on first non existing (check where I do fail earlierst, /w misspelling or diff language)




                
##might not need that -> better planning? is it WebContent?
class Word:
    def __init__(self, examplePhrase, pronounciation, picture, containedInList, ankiCard, lemmata):
        self.contained_in_list = containedInList
        self.lemmata = lemmata
        

###make this into a Module? everything todo with web?

class WebContent:
    #parent class for the below, check tim
    def __init__(self, URL, relevantHtml):
        self.url = URL
        self.relevant_html = relevantHtml
        
    def select_content(self):
        ##TODO: content (image, phrase, pronounciation?) manual choic
        return "user selected x content for Anki card"

class ExamplePhrase(WebContent):
    def __init__(self, URL, relevantHtml, word):
        super().__init__(URL, relevantHtml)
        self.word = word
        
    def highlight_word(self, word):
        ##TODO: word highlighting
        return "word x highlighted"
        
class Picture(WebContent):
    def __init__(self, URL,  relevantHtml, filepath):
        super().__init__(URL, relevantHtml)
        self.file_path = filepath
        
    def create_unique_name(self, filepath):
        ##TODO: check whether filename is unique
        return "Filename x is unique // had to rename file"

class Pronounciation(WebContent):
    def __init__(self, URL, relevantHtml):
        super().___init__(URL, relevantHtml)
        
    def play_audio(self):
        ##TODO: play audio content
        return "playing audio x"
    

class AnkiCard:
    def __init__(self, deck, content):
        self.deck_name = deck
        self.card_content = content
        
    def create_card(self, deck, content):
        ##TODO: card creation
        return "Anki Card created in deck x with content y"


class Session:
    def __init__(self, sourceFile, totalWordsRemaining):
        self.source_file = sourceFile
        self.words_remaining = totalWordsRemaining
        self.cards_made = 0
        self.words_added = 0
        
    def track_progress(self, ankiCard):
        ##TODO: progress tracking
        return "went through x words and made y cards"
    
    def end_session(self):
        ##TODO: end the session upon button press + make backups?
        return "session ended due to keystroke (q -> not Strg + C?)"
        
class SourceFile:
    def __init__(self, filepath, language):
        self.file_path = filepath
        self.language = language

    def make_backup(self, filepath):
        ##TODO: backup creation
        return "Made a backup in filepath"
    
    def add_lemata(self, word):
        ##TODO: add lemata to file
        return "added lemmata to file"
    
    def eliminate_duplicates(self, filepath, word):
        ##TODO: check for duplicates in file
        return "duplicate found, eliminated"
    


