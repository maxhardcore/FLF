import os
import time
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

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

    print(i, " items written to vocabulary file.")

    text_file.close()

def EpubScraper(filepath):
    scrapedlist=[]
    book = epub.read_epub(filepath)
    images = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    for item in images:
        if item.get_name() == 'frequency.xlink.xhtml':
            scrapedlist.append(item.get_content())
            #print(item.file_name," lol")
            #for line in item.get_content():
            #    print(line)
        #print(item.get_name())

    #print(scrapedlist, " rofl")
    #WriteNewDoc(scrapedlist, "epubscraper")
    return scrapedlist

def chap2text(chap):
#    output = ''
    output = []

    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            #output += '{} '.format(t)
            output.append(t)
    return output

#abändern auf liste, damit jedes item einzeln appended wird, sonst ist es eine sausage text

#def thtml2ttext(thtml):
#    Output = []
#
#    for html in thtml:
#        text = chap2text(html)
#        Output.append(text)
#    return Output

def epub2text(epub_path):
    chapters = EpubScraper(epub_path)

    ttext = thtml2ttext(chapters)
    #WriteNewDoc(ttext, "epubscraaper")
    return ttext


        #print(item)
    #all_items = book.get_items()
#
    #print(all_items)

def LookForContent(scrapedlist):
    grammarlist = ["art", "prep", "nm", "nf", "nc", "nm/f", "nmf", "conj", "v", "pron", "adv", "adj", "num", "interj", ]
    grammar = [x for x in scrapedlist if (x in grammarlist)]
    return grammar




#web = WebScraper("10000_formas.TXT")
#anki = AnkiScraper("E:\OneDrive\!Espanol\Ankiresoirces")
#lists =[web, anki]
#unlearnedwords = ListCompare(lists)
#lists.append(unlearnedwords)
#perseent = PercentageKnown((lists))
#stephenking = WriteNewDoc(lists, "10000_formas")

blacklist = [   '[document]',   'noscript', 'header',   'html', 'meta', 'head','input', 'script',   ]
freq = EpubScraper("FreqSpan.epub")


out=epub2text("FreqSpan.epub")
editedout = LookForContent(out)
print(out)

#todo: build mega list from all lists (immer if not in lists, und erweitern statt datum adden. oder beides, als backup.)
#todo: syntax vereinfachen
#todo: from url, nicht nur aus textfle


#todo: out zurechtschneiden: von ZAHL (i+=1) bis prep, adj, adv,...