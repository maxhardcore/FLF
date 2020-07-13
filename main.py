import os
import time
import ebooklib
from ebooklib import epub
from collections import defaultdict
import re

def WebScraper (URL: str):
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
    res = [x for x in lists[0] if x not in lists[1]]
    count = 0
    for i in res:
        count+=1
    print(count, " elements remaining after removal.")
    return res

def PercentageKnown(lists):
    weblen = len(lists[0])
    ankilen = len(lists[1])
    unlearnedlen= len(lists[2])
    percentageknown = [unlearnedlen/weblen, (weblen - unlearnedlen)/ankilen]
    print(percentageknown[0]*100, "% remaining from new source. ", round(percentageknown[1]*100,2), "% of Anki elements used.")
    return percentageknown

def WriteNewDoc(lists, sourcefile: str):
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
    scrapedlist=[]
    book = epub.read_epub(filepath)
    images = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    for item in images:
        if item.get_name() == 'frequency.xlink.xhtml':
            scrapedlist.append(item.get_content())
    return scrapedlist

def ReplaceSpecial(bookcontent):
    pattern = "bold\"\>(.*?)\<"
    for entry in bookcontent:
        entry = entry.decode("utf-8")
        rofl = re.findall(pattern, entry)
    del rofl[0]

    wordlist = []
    for eintrag in rofl:
        wordlist.append(eintrag.replace(u'\xa0', u''))

    wortliste = []
    i = 1
    for wort in wordlist:
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