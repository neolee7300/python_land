#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sys, os, re 
from bs4 import BeautifulSoup
from urllib.request import urlopen
from importlib import reload
# pickle save objects
import pickle,gzip
import subprocess

class Word_grabber:
    dict_web = 'https://www.merriam-webster.com/dictionary/'
    db_url = './dict_db.dict'
    dict_db = {}
    hard = 2 # The word that considered hard

    def __init__(self, output_string=''):
        self.output_string = output_string
        self.load_db()

    def show_text(self, text):
        text = os.linesep.join([s for s in text.splitlines() if s])   # remove empty lines
        text = re.sub('   *','\n\t',text) # replace continus space to  new line with a tab
        text = re.sub('\n:',':',text)    # If a line start with : , join the previouse line
        text = re.sub('\narchaic','  archaic',text) 
        
        text = os.linesep.join([s for s in text.splitlines() if s])   # remove empty lines        
        #text = " ".join([s for s in text.splitlines() if s])   # join lines
        #text = " ".join(text.split()) # remove multiple spaces 
        self.output_string += (text +'\n') 
        #print(text)

    def show_objs(self, objs):
        for idx,obj in enumerate(objs) :
            if not obj.find('script') :
                #self.show_text('Showing obj '+ str(idx) + '....... \n')
                self.show_text(obj.text)

    def load_db(self,url = None):
        url = url if url is not None else self.db_url 

        print('trying to get db from url --' + url + '\n')
        if os.path.isfile(url): 
            with gzip.open(url, 'rb') as f:
                self.dict_db = pickle.load(f)
                #return pickle.load(f)
            return self.dict_db
        else:
            print('url --' + url + ' is not there. \n')
            return {}

    # filter and return the words that checked more than "hard" times            
    def get_hard_words(self, hard = None) :
        hard = hard if hard is not None else self.hard 
        filtered_dict = {k:v for k,v in self.dict_db.items() if  
            v['times'] > hard}
        return filtered_dict

    def save_db(self, url=None):
        # set default value in class memthod
        url = url if url is not None else self.db_url 
        print('Saving db to url --' + url + '\n')
        with gzip.open(url , 'wb') as f:
            #pickle.dump(self.dict_db, f, 0)
            pickle.dump(self.dict_db, f, pickle.HIGHEST_PROTOCOL)

    def backup_db(self, url=None):
        # set default value in class memthod
        url = url if url is not None else self.db_url 
        url = '.' + url + '.bak'

        print('Backup db to url --' + url + '\n')
        self.save_db(url) 
        subprocess.call(['chmod', '0444', url])

    def update_db(self,word_lookup):
        self.dict_db[word_lookup]['times'] += 1
        print('\n******************************************')  
        print('"' + word_lookup + '" has been checked ' 
            + str(self.dict_db[word_lookup]['times']) + ' times')        
        print('******************************************\n')

    def reset_db_counts(self):
        for k, v in self.dict_db.items() :
            self.dict_db[k]['times'] = 0

    def query(self,word_lookup):
        if word_lookup in  self.dict_db :
            print(self.dict_db[word_lookup]['contents'])
            self.update_db(word_lookup)
            self.save_db()
        else:
            #self.grab_word_from_url(word_lookup)
            self.lynx_word_from_url(word_lookup)
            self.save_db()
            #print(self.dict_db[word_lookup]['contents'])
            print(self.dict_db[word_lookup]['contents'].decode())
            
    def lynx_word_from_url(self,word_lookup):
        try:
            url = self.dict_web + word_lookup
            #print(commands.getstatusoutput("cat syscall_list.txt | grep f89e7000 | awk '{print $2}'"))       
            cmd_str = 'lynx -dump -notitle -dont_wrap_pre -width=990 -nolist  ' + '"' + url  + '"'     
  
            self.output_string= subprocess.check_output(cmd_str, shell=True)
            self.dict_db.update({word_lookup:{'contents':self.output_string,'times':0}})
            self.update_db(word_lookup)
            # clean the output_string for next word
            self.output_string = ''
            return 'found'    
        except AttributeError:
            print( "word can not be found")
            return 'not found'
            #sys.exit(2)
    
        except TypeError:
            print ("NA")
            return 'wrong type'                    

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
            return 'found'
    
        except AttributeError:
            print( "word can not be found")
            return 'not found'
            #sys.exit(2)
    
        except TypeError:
            print ("NA")
            return 'wrong type'

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
    wg.query(word_lookup)
    

if __name__ == '__main__':
    main()
