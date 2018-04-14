#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sys, os, re 
from bs4 import BeautifulSoup
# For Python 3.0 and later
from urllib.request import urlopen
from importlib import reload
# pickle save objects
import pickle

class Word_grabber:
    dict_web = 'https://www.merriam-webster.com/dictionary/'

    db_url = './dict_db.dict'

    dict_db = {}

    def __init__(self, output_string):
        self.output_string = output_string

    def show_text(self, text):
        text = os.linesep.join([s for s in text.splitlines() if s])   # remove empty lines
        text = re.sub('   *','\n\t',text) # replace continus space to  new line with a tab
        text = re.sub('\n:',':',text)    # If a line start with : , join the previouse line
        text = re.sub('\narchaic','  archaic',text) 
        
        text = os.linesep.join([s for s in text.splitlines() if s])   # remove empty lines        
        #text = " ".join([s for s in text.splitlines() if s])   # join lines
        #text = " ".join(text.split()) # remove multiple spaces 
        self.output_string += (text +'\n') 
        print(text)

    def show_objs(self, objs):
        for idx,obj in enumerate(objs) :
            if not obj.find('script') :
                #self.show_text('Showing obj '+ str(idx) + '....... \n')
                self.show_text(obj.text)

    def load_db(self,url = None):
        url = url if url is not None else self.db_url 

        print('trying to get db from url --' + url + '\n')
        if os.path.isfile(url): 
            with open(url, 'rb') as f:
                self.dict_db = pickle.load(f)
                #return pickle.load(f)
        else:
            print('url --' + url + ' is not there. \n')


    def save_db(self, url=None):
        # set default value in class memthod
        url = url if url is not None else self.db_url 
        print('trying to save db to url --' + url + '\n')
        with open(url , 'wb') as f:
            pickle.dump(self.dict_db, f, 0)
            #pickle.dump(self.dict_db, f, pickle.HIGHEST_PROTOCOL)

    def update_db(self,word_lookup):
        self.dict_db[word_lookup]['times'] += 1
        print('\n******************************************')  
        print('"' + word_lookup + '" has been checked ' 
            + str(self.dict_db[word_lookup]['times']) + ' times')        
        print('******************************************\n')

    def grab_word_from_url(self,word_lookup):
        try:
            page = urlopen(self.dict_web + word_lookup)
            #result = f.read()
            soup = BeautifulSoup(page, 'html.parser')
            self.soup = soup 
            #print(soup.prettify())

            self.show_text('\n' + '\t \t' + word_lookup + '\n') 
            # pronunciation section
            self.show_text('***********************************\n')  
            text = soup.body.find('div', attrs={'class' : 'entry-attr'}).text
            text = os.linesep.join([s for s in text.splitlines() if s])   # remove empty lines
            text = " ".join(text.split()) # remove multiple spaces 
            self.show_text(text)

            # meaning section
            self.show_text('**********meaning******************\n') 
            objs = soup.find_all('div', attrs={'class' : 'vg'})
            self.show_objs(objs)

            # exsamples section
            self.show_text('**********examples*****************\n') 
            objs = soup.find_all('ol', attrs={'class' : 'definition-list no-count'})
            self.show_objs(objs)

            print(' \nTrying to add word into db')
            self.dict_db.update({word_lookup:{'contents':self.output_string,'times':0}})
            print(' Word is in db')

            self.update_db(word_lookup)
            # clean the output_string for next word
            self.output_string = ''
    
        except AttributeError:
            print( "word can not be found")
            sys.exit(2)
    
        except TypeError:
            print ("NA")

def main():
    reload(sys)                         # 2
    wg = Word_grabber('') 
    print('web url is ' + wg.dict_web + '\n')

    if len(sys.argv) == 2:
        word_lookup = sys.argv[1]
    else:
        print ('What do you want to look up?')
        sys.exit(1)

    wg.load_db()
    if word_lookup in  wg.dict_db :
        print(wg.dict_db[word_lookup]['contents'])
        wg.update_db(word_lookup)
        wg.save_db()
    else:
        wg.grab_word_from_url(word_lookup)
        wg.save_db()

if __name__ == '__main__':
    main()
