#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sys, os 
from bs4 import BeautifulSoup
# For Python 3.0 and later
from urllib.request import urlopen
from importlib import reload
# pickle save objects
import pickle

class Word_grabber:
    dict_web = 'https://www.merriam-webster.com/dictionary/'

    db_url = './dict_db.dict'

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

    def save_db(self, url=None):
        # set default value in class memthod
        url = url if url is not None else self.db_url 
        with open(url , 'wb') as f:
            pickle.dump(self.dict_db, f, pickle.HIGHEST_PROTOCOL)

    def update_db(self,word_lookup):
         print(self.dict_db[word_lookup]['contents'])
         self.dict_db[word_lookup]['times'] += 1
         print(self.dict_db[word_lookup]['times'])

    def grab_word_from_url(self,word_lookup):
        try:
            page = urlopen(self.dict_web + word_lookup)
            #result = f.read()
            soup = BeautifulSoup(page, 'html.parser')
            #print(soup.prettify())

            self.show_text('\n' + '\t \t' + word_lookup + '\n') 
            # pronunciation section
            self.show_text('*************************************')  
            text = soup.body.find('div', attrs={'class' : 'entry-attr'}).text
            text = os.linesep.join([s for s in text.splitlines() if s])   # remove empty lines
            text = " ".join(text.split()) # remove multiple spaces 
            self.show_text(text)

            # meaning section
            self.show_text('\n**********meaning******************') 
            objs = soup.find_all('div', attrs={'class' : 'vg'})
            self.show_objs(objs)

            # exsamples section
            self.show_text('\n**********examples*****************') 
            objs = soup.find_all('ol', attrs={'class' : 'definition-list no-count'})
            self.show_objs(objs)
    
        except AttributeError:
            print( "word can not be found")
            sys.exit(2)
    
        except TypeError:
            print ("NA")

def main():
    reload(sys)                         # 2
    wg = Word_grabber('') 
    wg.show_text('web url is ' + wg.dict_web)

    if len(sys.argv) == 2:
        word_lookup = sys.argv[1]
    else:
        print ('What do you want to look up?')
        sys.exit(1)

    if word_lookup in  wg.dict_db :
        wg.update_db(word_lookup)
    else:
        wg.grab_word_from_url(word_lookup)
        wg.save_db


if __name__ == '__main__':
    main()
