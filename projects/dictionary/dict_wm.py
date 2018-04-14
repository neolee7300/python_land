#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sys, os 
from bs4 import BeautifulSoup
# For Python 3.0 and later
from urllib.request import urlopen
from importlib import reload

class Word_grabber:
    dict_web = 'https://www.merriam-webster.com/dictionary/'

    dict_db = {'lion': {'contents': "hello", 'times' : 1 } }
    def __init__(self, output_string):
        self.output_string = output_string

    def show_text(self, text):
        text = os.linesep.join([s for s in text.splitlines() if s])   # remove empty lines
        #text = " ".join([s for s in text.splitlines() if s])   # join lines
        #text = " ".join(text.split()) # remove multiple spaces 
        self.output_string += text
        print(text)

    def show_objs(self, objs):
        for obj in objs :
            if not obj.find('script') :
                self.show_text(obj.text)

    def get_db(self,url):
        print('trying to get db from url --' + url + '\n')

    def save_db(self,url):
        print('trying to save db to url --' + url + '\n')

def main():
    reload(sys)                         # 2
    wg = Word_grabber('') 
    wg.show_text('web url is ' + wg.dict_web)

    try:
        if len(sys.argv) == 2:
            word_lookup = sys.argv[1]
        else:
            print ('What do you want to look up?')
            sys.exit(1)

        if word_lookup in  wg.dict_db :
            print(wg.dict_db[word_lookup]['contents'])
            wg.dict_db[word_lookup]['times'] += 1
            print(wg.dict_db[word_lookup]['times'])
           
        page = urlopen(wg.dict_web + word_lookup)
        #result = f.read()
        soup = BeautifulSoup(page, 'html.parser')
        #print(soup.prettify())

        wg.show_text('\n' + '\t \t' + word_lookup + '\n') 
        # pronunciation section
        wg.show_text('*************************************')  
        text = soup.body.find('div', attrs={'class' : 'entry-attr'}).text
        text = os.linesep.join([s for s in text.splitlines() if s])   # remove empty lines
        text = " ".join(text.split()) # remove multiple spaces 
        wg.show_text(text)

        # meaning section
        wg.show_text('\n**********meaning******************') 
        objs = soup.find_all('div', attrs={'class' : 'vg'})
        wg.show_objs(objs)

        # exsamples section
        wg.show_text('\n**********examples*****************') 
        objs = soup.find_all('ol', attrs={'class' : 'definition-list no-count'})
        wg.show_objs(objs)

    except AttributeError:
        print( "word can not be found")
        sys.exit(2)

    except TypeError:
        print ("NA")

if __name__ == '__main__':
    main()
