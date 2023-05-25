# -*- coding: utf-8 -*-
"""
Created on Tue May 16 21:44:31 2023

@author: Linus
"""

from anki.storage import Collection 

def create_card(image, sentence, audio, anki_collection_path, anki_model_name, anki_deck_name):    
    # 1. Load the anki collection 
    col = Collection(anki_collection_path, log=True)
    
    # 2. Select the deck 
    
    # Find the model to use (Basic, Basic with reversed, ...)
    
    modelBasic = col.models.by_name(anki_model_name)
    ##col.models.all_names_and_ids() # how to find it
    #"2. Picture Words""
    #or "Arabic"

    # Set the deck
    deck = col.decks.by_name(anki_deck_name)
    ##col.decks.all_names_and_ids() # how to find it
    #"Espanol", id 1553808892755
    #Lisaan Masri, id 1661077163888
    
    col.decks.select(deck['id'])
    col.decks.current()['mid'] = modelBasic['id']
    
    # 3. Create a new card 
    note = col.newNote()
    note.fields[0] = sentence
    note.fields[1] = image
    col.addNote(note)
    
    # 4. Close the collection
    col.close()
    
# create_card("img", "phrase", "audio", r'C:\Users\Linus\AppData\Roaming\Anki2\User 1\collection.anki2', "2. Picture Words", "Espanol")

##deck override?, now on -> maybe?