#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sys, os, re 
from bs4 import BeautifulSoup
from urllib.request import urlopen
from importlib import reload
# pickle save objects
import pickle,gzip,json

import read_english_dictionary 
import dict_wm 

import random
from time import sleep

def create_new_words(english_words):

    wg = dict_wm.Word_grabber('')
    new_words={}
    new_words=wg.load_db('./new_words.dict')
    
    random_keys=list(english_words.keys())    
    random.shuffle(random_keys)

    for key in random_keys:
        new_words.update({key:{'contents':'','times':-1}})
        
    wg.dict_db=new_words    
    wg.save_db('./new_words.dict')
      
    

if __name__ == '__main__':
    english_words = read_english_dictionary.load_words()
    wg = dict_wm.Word_grabber('')

    new_words=wg.load_db('./new_words.dict')
    wrong_words=wg.load_db('./wrong_words.dict')
    wg.dict_db = wg.load_db('./dict_db.dict')    
    
    while new_words :
        for x in range(1, 500) :
            word = new_words.popitem()[0]
            print('checking ' + word + '  ' +str(len(new_words)) + ' words left')
            print('left %d , right %d, wrong %d' % (len(new_words), len(wg.dict_db), len(wrong_words)))                         
            #sleep(random.randint(1,2))
            try:
                result = wg.lynx_word_from_url(word)
                #print('checked ' + word + '  ' +str(len(new_words)) + ' words left')
            except:
                wrong_words.update({word:{'contents':'','times':-1}})
                pass
            
        print('saving' + str(len(wg.dict_db)) + " good words ");
        good_words = wg.dict_db;
        wg.save_db('./dict_db.dict')        

        wg.dict_db=wrong_words
        #print(wrong_words.keys())
        print('saving' + str(len(wg.dict_db)) + " wrong words ");
        wg.save_db('./wrong_words.dict')    
        
        wg.dict_db=new_words    
        print('saving' + str(len(wg.dict_db)) + " new words ");
        wg.save_db('./new_words.dict')
        wg.dict_db=good_words;        
          
