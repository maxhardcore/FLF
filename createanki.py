# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 21:30:42 2021

@author: Linus
"""

#https://github.com/kerrickstaley/genanki
import os
# import clipboardgrabba as cbg
from anki.storage import Collection 
import reversoApi
from bs4 import BeautifulSoup
from requests import get

class Note(object):
    def __init__(self, sentence, image):
        self.Sentence = sentence
        self.Image = image
 


def CreateSingleCard(image, sentence):

    # Find the Anki directory 
    anki_home = r'C:\Users\Linus\AppData\Roaming\Anki2\User 1'
    anki_collection_path = os.path.join(anki_home, "collection.anki2")
    
    # 1. Load the anki collection 
    col = Collection(anki_collection_path, log=True)
    
    # 2. Select the deck 
    
    # Find the model to use (Basic, Basic with reversed, ...)
    modelBasic = col.models.byName('2. Picture Words')
    # Set the deck
    deck = col.decks.byName('Espanol')
    col.decks.select(deck['id'])
    col.decks.current()['mid'] = modelBasic['id']
    
    # 3. Create a new card 
    note = col.newNote()
    note.fields[0] = "jesge jü" # The Front input field in the U
    ###has to be in collection.models (AppData/Roaming)
    note.fields[1] = '<img src="{0}.jpg">'.format(image)   # The Back input field in the UI
    col.addNote(note)
    
    # 4. Save changes 
    col.close()
    print('Card created: ', sentence)
    

def CreateBatchCards(notes):
    ##notes is a list of dicts
    notes = [ 
      {
        "Front": "Bonjour",
        "Back": "Hello",
      },
      {
        "Front": "Merci",
        "Back": "Thank you",
      },
      # Thousands of additional notes...
    ]
    
    # Find the Anki directory
    anki_home = r'C:\Users\Linus\AppData\Roaming\Anki2\User 1'
    anki_collection_path = os.path.join(anki_home, "collection.anki2")
    
    # 1. Load the anki collection
    col = Collection(anki_collection_path, log=True)
    
    # 2. Select the deck
    # Find the model to use (Basic, Basic with reversed, ...)
    modelBasic = col.models.byName('2. Picture Words')
    # Set the deck
    deck = col.decks.byName('Espanol')
    col.decks.select(deck['id'])
    col.decks.current()['mid'] = modelBasic['id']
    
    # 3. Create the cards
    for current_note in notes: 
      note = col.newNote()
      note.fields[0] = current_note["Front"]
      note.fields[1] = current_note["Image"]
      col.addNote(note)
    
    # 4. Save changes
    col.close()
    
# def CreateNotes():
#     noteArray = [Note("Nick", "Programmer"), Note("Alice","Engineer")]
#     notesList = [dict(n.Sentence, n.Image) for n in noteArray]
#     return notesList

def CreateNotes(noteArray):
    # noteArray = [Note("Nick", "Programmer"), Note("Alice","Engineer")]
    notesList = [dict(Front = n[2], Back = n[1]) for n in noteArray]
    return notesList

    
    ##create a dict for every sentence, image I pick, and print it out at every step? or log it somewhere?
    #so I have a backup to ctr c / v into python in case sth. goes wrong.
    #maybe make a folder: list & images -> then batch create notes, delete folder afterwards
    #that way I can also do it in steps and then batch create notes.
    
    
    
    

# CreateSingleCard('schlurl', 'schluuurl')
# CreateBatchCards(notes = [])
# u = CreateNotes()

searchWord = 'leña'
url = "https://context.reverso.net/traduccion/espanol-aleman/" + searchWord
headers = {'User-Agent': 'Mozilla/5.0'}
response = get(url, headers = headers)
soup = BeautifulSoup(response.text, 'html.parser')


y = reversoApi.FrequencyOfTranslation()
w = reversoApi.PickTranslations(y)
if w:
    z= reversoApi.GetExampleSentences(searchWord, w)
else:
    print(' did not pick any word')
a = reversoApi.PickSentences(searchWord, z)
b= CreateNotes(a)
print('refl')
#https://www.youtube.com/watch?v=QZn_ZxpsIw4

#https://www.juliensobczak.com/write/2020/12/26/anki-scripting-for-non-programmers.html

#https://levelup.gitconnected.com/how-to-download-google-images-using-python-2021-82e69c637d59
##this might work, changing the image url (xpath) to what user inputs! 

