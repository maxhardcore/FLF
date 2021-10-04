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
from selenium import webdriver
from shutil import copy
# import clipboardgrabba

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
    
    #trying this
    ###trying this 

    modelBasic = col.models.byName('2. Picture Words')

    # Set the deck
    deck = col.decks.byName('Espanol')
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
    # print('Card created: ', sentence)
    

def CreateBatchCards(noteList):
    ##notes is a list of dicts
    # notes = [ 
    #   {
    #     "Front": "Bonjour",
    #     "Back": "Hello",
    #   },
    #   {
    #     "Front": "Merci",
    #     "Back": "Thank you",
    #   },
    #   # Thousands of additional notes...
    # ]
    
    notez = CreateNotes(noteList)
    
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
    for current_note in notez: 
      note = col.newNote()
      note.fields[0] = current_note["Front"]
      note.fields[1] = current_note["Image"]
      col.addNote(note)
      # print('Card created: ', note.fields[0])
    
    # 4. Save changes
    col.close()
    
# def CreateNotes():
#     noteArray = [Note("Nick", "Programmer"), Note("Alice","Engineer")]
#     notesList = [dict(n.Sentence, n.Image) for n in noteArray]
#     return notesList

def CreateNotes(noteArray):
    # noteArray = [Note("Nick", "Programmer"), Note("Alice","Engineer")]
    if len(noteArray) > 1:
        notesList = [dict(Front = n[2], Image = n[4]) for n in noteArray]
    else:
        notesList = [dict(Front = v[2], Image = v[4]) for n in noteArray for v in n]
    return notesList

    
    ##create a dict for every sentence, image I pick, and print it out at every step? or log it somewhere?
    #so I have a backup to ctr c / v into python in case sth. goes wrong.
    #maybe make a folder: list & images -> then batch create notes, delete folder afterwards
    #that way I can also do it in steps and then batch create notes.
    
def GoThroughList(file):
    f = open(file, "r")
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
    # print("Backing up ", file)
    copy(ogLocation+"\\"+file, filePath)
    return filePath

    
    
    

def DelWords(file, deleteThisWord):
    with open(file, "r") as f:
        lines = f.readlines()
    # addedWords = [v[0] for n in noteArray for v in n]
    with open(file, "w") as f:
        for line in lines:
            #only writes those that are not yet added, thus eliminates added words.
            if line.strip("\n") != deleteThisWord:
                if line.strip("\n") != "":
                    f.write(line)
                # print('deleted word ', line.strip("\n"))
    
    

# CreateSingleCard('schlurl', 'schluuurl')
# CreateBatchCards(notes = [])
# u = CreateNotes()


browser = webdriver.Firefox()
browser.install_addon(r'C:\E\OneDrive\!!!PyProjects\FLF\view_image_context_menu_item-1.3-fx.xpi')
browser.minimize_window()
headers = {'User-Agent': 'Mozilla/5.0'}
sourcefile = 'atesta.txt'
BackupFile(sourcefile)
u = GoThroughList(sourcefile)
# for searchWord in u:
#     a = reversoApi.PickSentences(searchWord, browser, sourcefile)



# a=[]
cardCounter = 0
try:
    while True:
        if u:
        # a = [reversoApi.PickSentences(searchWord, browser) for searchWord in u]
            for searchWord in u:
                if searchWord != "":
                    a = reversoApi.PickSentences(searchWord, browser, sourcefile)
                    # a.append(reversoApi.PickSentences(searchWord, browser, sourcefile))
                    u.remove(searchWord)
                    if a:
                        if len(a) > 1:
                            cardCounter+= len(a)
                            CreateBatchCards(a)
                        else:
                            cardCounter +=1
                            CreateSingleCard(a[0][4], a[0][2])
                        DelWords(sourcefile, a[0][0])
                    
        else:
            print('finished, no more words available')
            # DelWords(sourcefile, a)
            break
except KeyboardInterrupt:
    # DelWords(sourcefile, a)
    pass
# b= CreateNotes(a)
# print(len(a)-1, "cards added to Anki")
print(cardCounter, "cards added to Anki")
print(reversoApi.CountNonexisting(), ' deleted as no translation found')
u = GoThroughList(sourcefile)
if u:
    print(len(u), "words with spelling corrected, run again.")
print("SWITCH DECKS")
# CreateBatchCards(a)
browser.quit()

print('refl')
#https://www.youtube.com/watch?v=QZn_ZxpsIw4

#https://www.juliensobczak.com/write/2020/12/26/anki-scripting-for-non-programmers.html

#https://levelup.gitconnected.com/how-to-download-google-images-using-python-2021-82e69c637d59
##this might work, changing the image url (xpath) to what user inputs! 

