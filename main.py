import os
import time
import ebooklib
from ebooklib import epub
import re
import numpy as np
import spacy
from spacy_spanish_lemmatizer import SpacyCustomLemmatizer
import collections
import keyboard


def WebScraper (URL: str):
    #Supposed to scrape a websource. As of know, scrapes from txt document.
    scrapedlist=[]
    file_object = open(URL, "r")

    for line in file_object:
        scrapedlist.append(line.split()[1])
    scrapedlist_sorted = sorted(scrapedlist)
    count=len(scrapedlist_sorted)
    print(count, " elements scraped from web source.")
    return scrapedlist_sorted

def AnkiScraper(folder: str):
    #Scrapes the Anki folder, returns a list of words already in Anki database
    filenames = os.listdir(folder)
    scrapedlist = []
    for file in filenames:
        scrapedlist.append(file.rsplit(".")[0])
    #Remove all digits (since words with multiple meanings are numbered)
    pattern = '[0-9]'
    scrapedlist = [re.sub(pattern, '', i) for i in scrapedlist]
    #Sorts alphabetically
    scrapedlist_sorted = sorted(scrapedlist)

    #Removes duplicates
    scra = list(dict.fromkeys(scrapedlist_sorted))
    count=len(scra)
    print(count, " elements currently in Anki database.")
    return scra

def ListCompare(lists):
    #gives amount of words not yet known (non-duplicates)
    #returns a set of all unlearned words
    res =[]
    for i in range(len(lists)):
        for j in range(len(lists[i])):
            res.append(lists[i][j])
    unique = set(res)
    count = len(unique)
    #res = [x for x in lists[0] if x not in lists[1]]
    print(count, " elements remaining after removal of duplicates.")
    return unique



def PercentageKnown(lists):
    #Compares known (in Anki folder) to scraped (from various sources) content; gives percentage known
    weblen = len(lists[0]) # 10000: length of textfile scraped
    ankilen = len(lists[1]) # 5000: length of words in Kindle source
    unlearnedlen= len(lists[2]) # unique words in the above (11036)
    percentageknown = [unlearnedlen/(weblen+ankilen), (weblen - unlearnedlen)/ankilen]
    print(percentageknown[0]*100, "% remaining from new source. ")
    return percentageknown

def WriteNewDoc(list, sourcefile: str):
    #Creates a .txt file with the scraped content; name containts date and time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    text_file = open(sourcefile + timestr + ".txt", "w")
    j=0

    for item in list:
        j+=1
            #text_file.write(item + "\n")
        text_file.write(str(item))
        text_file.write("\n")

    print(j, " items written to vocabulary file.")

    text_file.close()

def EpubScraper(filepath):
    #Creates a list of the content in the Ebook.
    scrapedlist=[]
    book = epub.read_epub(filepath)
    #Only document (text) content
    images = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    for item in images:
        #Specifying the name of the chapter / content type to be scraped hardcoded
        if item.get_name() == 'frequency.xlink.xhtml':
            scrapedlist.append(item.get_content())
    return scrapedlist

def ReplaceSpecial(bookcontent):
    #Replaces all special Characters in the scraped content. Also filters the entire string for desired values
    #String hardcoded due to specific format of Frequency Dictionary Spanish:
    #Desired content is betweeen 'bold">' and '\<'
    pattern = "bold\"\>(.*?)\<"
    for entry in bookcontent:
        # Removes all Hexcode-characters
        entry = entry.decode("utf-8")
        rofl = re.findall(pattern, entry)
    #First entry is a header, not pertaining to my interest
    del rofl[0]

    wordlist = []
    for eintrag in rofl:
    #Replace hexcoded spaces ('\xa0') with empty
        wordlist.append(eintrag.replace(u'\xa0', u''))

    wortliste = []
    i = 1
    for wort in wordlist:
    #Removes the leading number (since entries are numbered by their frequency)
        wortliste.append(wort.replace(str(i), u''))
        i += 1
    print(len(wortliste), " words from Kindle source")
    return wortliste

def Lemmatizer(filename):
    #Uses SpaCy's Lemmatizer (submodel: Espanol) to lemmatize entries
    #todo: nach haeufigkeit sortieren
    f = open(filename, "r")
    nlp = spacy.load("es_core_news_sm")
    lemmatizer = SpacyCustomLemmatizer()
    nlp.add_pipe(lemmatizer, name="lemmatizer", after="tagger")

    #reads in document and lemmatizes each line
    uniquelemmas = []
    i = 0
    j = 0
    for line in f:
        for token in nlp(line):
            if token.text !="\n":
                if token.lemma_ != token.text:
                    uniquelemmas.append(token.lemma_)
                    print(token.lemma_, " added")
                    i+=1
                else:
                    uniquelemmas.append(token.lemma_ +  " unchanged")
                    print(token.lemma_, " added")
                    j+=1

    counts = collections.Counter(uniquelemmas)
    new_list = sorted(counts, key=counts.get, reverse=True)
    print(j, " words unchanged")
    print(len(new_list) + j, " total items")

    return new_list

def CompareLemmas(lemmatized, ankidict):
    f = open(lemmatized, "r")
    #strips all '\n' and ' unchanged'
    stripped = []
    for line in f:
        strippedline = line.rstrip("\n")

        if re.search(r'\bunchanged\b', strippedline):
            stripped.append(strippedline[:-10])
        else:
            stripped.append(strippedline)

    unique = [i for i in stripped if i not in ankidict]
    return unique

def RemoveParticipio(lemmalist):
    #Asks user which words endlich in -ido, -ado, -ito to remove
    #Has to be done manually but will save time
    f = open(lemmalist, "r")
    cleanedup = []
    i=1
    for line in f:
        print(i)
        i+=1
        print("Checking " + line + "...")
        strippedline = line.rstrip("\n")
        if strippedline[-2:] == "do" or strippedline[-2:] == "to":
            print("DELETE " + strippedline + " ? [q: keep, ELSE: delete]")
            if input() == "q":
                print(line + " kept")
                cleanedup.append(strippedline)
            else:
                print(strippedline + " deleted")

        else:
            cleanedup.append(strippedline)
    return cleanedup









##http://corpus.rae.es/frec/10000_formas.TXT
#web = WebScraper("10000_formas.TXT")
#
##already in folder (unique entries only)
#anki = AnkiScraper("E:\OneDrive\!Espanol\Ankiresoirces")
##ahogar: 145 ahogar2: 146
#
##all the words in the kindle frequency dictionary
FreqDictKindle = ReplaceSpecial(EpubScraper("FreqSpan.epub"))
#
#lists =[web, FreqDictKindle]
#unlearnedwords = ListCompare(lists)
#lists.append(unlearnedwords)
#perseent = PercentageKnown((lists))
#ankiset = set(anki)
#newwords= list(lists[2]-ankiset)
#
#stephenking = WriteNewDoc(newwords, "NewWordsEspanol")


#Lemmatize words and write them to a new file
#uniklemmas = Lemmatizer("espa.txt")
#stephenking = WriteNewDoc(uniklemmas, "LemmasEspanol")


#uniquelemmas = CompareLemmas("lemmatizedesp.txt", FreqDictKindle)
#
#stephenking = WriteNewDoc(uniquelemmas, "UniquelLemmas_Unlearned_newmethod")

cleanup = RemoveParticipio(("ToAdd - Kopie.txt"))
stephenking = WriteNewDoc(cleanup, "RemovedParti")





print("lol")
#todo: build mega list from all lists (immer if not in lists, und erweitern statt datum adden. oder beides, als backup.)
#todo: syntax vereinfachen
#todo: from url, nicht nur aus textfle

