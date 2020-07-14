import os
import time
import ebooklib
from ebooklib import epub
from collections import defaultdict
import re

def WebScraper (URL: str):
    #Supposed to scrape a websource. As of know, scrapes from txt document.
    scrapedlist=[]
    file_object = open(URL, "r")

    for line in file_object:
        scrapedlist.append(line.split()[1])
    count=0
    for i in scrapedlist:
        count+=1
    print(count, " elements scraped from web source.")
    return scrapedlist

def AnkiScraper(folder: str):
    #Scrapes the Anki folder, returns a list of words already in Anki database
    filenames = os.listdir(folder)
    scrapedlist = []
    for file in filenames:
        scrapedlist.append(file.rsplit(".")[0])
    count=0
    for i in scrapedlist:
        count+=1
    print(count, " elements currently in Anki database.")
    return scrapedlist

def ListCompare(lists):
    #gives amount of words not yet known (non-duplicates)
    res = [x for x in lists[0] if x not in lists[1]]
    count = 0
    for i in res:
        count+=1
    print(count, " elements remaining after removal.")
    return res

def PercentageKnown(lists):
    #Compares known (in Anki folder) to scraped (from various sources) content; gives percentage known
    weblen = len(lists[0])
    ankilen = len(lists[1])
    unlearnedlen= len(lists[2])
    percentageknown = [unlearnedlen/weblen, (weblen - unlearnedlen)/ankilen]
    print(percentageknown[0]*100, "% remaining from new source. ", round(percentageknown[1]*100,2), "% of Anki elements used.")
    return percentageknown

def WriteNewDoc(lists, sourcefile: str):
    #Creates a .txt file with the scraped content; name containts date and time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    text_file = open(sourcefile + timestr + ".txt", "w")
    j=0
    for i in range(len(lists)):
        for item in lists[i]:
            j+=1
            #text_file.write(item + "\n")
            text_file.write(str(item))
            text_file.write("\n")

    print(i, " items written to vocabulary file.")

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
    return wortliste


def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def list_duplicates(seq):
        tally = defaultdict(list)
        for i, item in enumerate(seq):
            tally[item].append(i)
        return ((key, locs) for key, locs in tally.items()
                if len(locs) > 1)
        reddit = []
        for dup in sorted(list_duplicates(scrapedlist)):
            reddit.append(dup)
        return reddit





#web = WebScraper("10000_formas.TXT")
#anki = AnkiScraper("E:\OneDrive\!Espanol\Ankiresoirces")
#lists =[web, anki]
#unlearnedwords = ListCompare(lists)
#lists.append(unlearnedwords)
#perseent = PercentageKnown((lists))
#stephenking = WriteNewDoc(lists, "10000_formas")


freq = EpubScraper("FreqSpan.epub")
rofl = ReplaceSpecial(freq)

#compton = list_duplicates(bup)



print("lol")
#todo: build mega list from all lists (immer if not in lists, und erweitern statt datum adden. oder beides, als backup.)
#todo: syntax vereinfachen
#todo: from url, nicht nur aus textfle