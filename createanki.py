# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 21:30:42 2021

@author: Linus
"""

import os
from anki.storage import Collection 
import reversoApi
from selenium import webdriver
from shutil import copy

class Note(object):
    def __init__(self, sentence, image):
        self.Sentence = sentence
        self.Image = image
 


def CreateSingleCard(image, sentence):
# def CreateSingleCard(noteList):
    # Find the Anki directory 
    anki_home = r'C:\Users\Linus\AppData\Roaming\Anki2\User 1'
    anki_collection_path = os.path.join(anki_home, "collection.anki2")
    
    # 1. Load the anki collection 
    col = Collection(anki_collection_path, log=True)
    
    # 2. Select the deck 
    
    # Find the model to use (Basic, Basic with reversed, ...)
    
    modelBasic = col.models.by_name('2. Picture Words')

    # Set the deck
    deck = col.decks.by_name('Espanol')
    col.decks.select(deck['id'])
    col.decks.current()['mid'] = modelBasic['id']
    
    # 3. Create a new card 
    note = col.newNote()
    note.fields[0] = sentence # The Front input field in the U
    ###has to be in collection.models (AppData/Roaming)
    # note.fields[1] = '<img src="{0}.jpg">'.format(image)   # The Back input field in the UI
    note.fields[1] = image
    col.addNote(note)
    
    # 4. Save changes 
    col.close()


def CreateBatchCards(noteList):

    
    notez = CreateNotes(noteList)
    
    # Find the Anki directory
    anki_home = r'C:\Users\Linus\AppData\Roaming\Anki2\User 1'
    anki_collection_path = os.path.join(anki_home, "collection.anki2")
    
    # 1. Load the anki collection
    col = Collection(anki_collection_path, log=True)
    
    # 2. Select the deck
    # Find the model to use (Basic, Basic with reversed, ...)
    modelBasic = col.models.by_name('2. Picture Words')
    # Set the deck

    
    
    
    
    deck = col.decks.by_name('Espanol')
    col.decks.select(deck['id'])
    col.decks.current()['mid'] = modelBasic['id']
    
    # 3. Create the cards
    for current_note in notez: 
      note = col.newNote()
      note.fields[0] = current_note["Front"]
      note.fields[1] = current_note["Image"]
      col.addNote(note)

    # 4. Save changes
    col.close()
    

def CreateNotes(noteArray):
    if len(noteArray) > 1:
        notesList = [dict(Front = n[2], Image = n[4]) for n in noteArray]
    else:
        notesList = [dict(Front = v[2], Image = v[4]) for n in noteArray for v in n]
    return notesList

    
def GoThroughList(file):
    f = open(file, "r",encoding="utf-8")
    lines = f.readlines()
    strippedlines = [line.strip() for line in lines]
    f.close()    
    return strippedlines

def BackupFile(file):
    ogLocation = r'C:\E\OneDrive\!!!PyProjects\FLF'
    backupLocation = r'C:\E\OneDrive\!!!PyProjects\FLF\backup'
    base, extension = os.path.splitext(file)
    filePath = os.path.join(backupLocation, base + extension)
    i=1
    if os.path.exists(filePath):
        while True:
            newpath = "{0}{2}{1}".format(*os.path.splitext(filePath) + (i,))
            if os.path.exists(newpath):
                i+=1
            else:
                copy(ogLocation+"\\"+file, newpath)
                return newpath
    copy(ogLocation+"\\"+file, filePath)
    return filePath

    
    
    

def DelWords(file, deleteThisWord):
    with open(file, "r",encoding="utf-8") as f:
        lines = f.readlines()
    with open(file, "w",encoding="utf-8") as f:
        for line in lines:
            #only writes those that are not yet added, thus eliminates added words.
            if line.strip("\n") != deleteThisWord:
                if line.strip("\n") != "":
                    f.write(line)
    
    



browser = webdriver.Firefox()
browser.install_addon(r'C:\E\OneDrive\!!!PyProjects\FLF\view_image_context_menu_item-1.3-fx.xpi')
browser.minimize_window()
headers = {'User-Agent': 'Mozilla/5.0'}
sourcefile = 'nonreflex_utf8.txt'
BackupFile(sourcefile)
u = GoThroughList(sourcefile)

#test

cardCounter = 0
wordCounter = 0
try:
    while True:
        if u:
            totalWords = len(u)
            for searchWord in u:
                wordCounter += 1
                if searchWord != "":
                    print(wordCounter, ' out of ', totalWords, 'words, that is ', "{:.2f}".format((wordCounter/totalWords)*100), ' percent' )
                    a = reversoApi.PickSentences(searchWord, browser, sourcefile)
                    u.remove(searchWord)
                    if a:
                        if len(a) > 1:
                            cardCounter+= len(a)
                            CreateBatchCards(a)
                        else:
                            cardCounter +=1
                            CreateSingleCard(a[0][4], a[0][2])
    
                        DelWords(sourcefile, a[0][0])
                    print(cardCounter, "cards added to Anki")
                    
        else:
            print('finished, no more words available')
            break
except KeyboardInterrupt:
    pass

print(cardCounter, "cards added to Anki")
print(reversoApi.CountNonexisting(), ' deleted as no translation found')
u = GoThroughList(sourcefile)
if u:
    print(len(u), "words with spelling corrected, run again.")
print("SWITCH DECKS")
browser.quit()

print('refl')


