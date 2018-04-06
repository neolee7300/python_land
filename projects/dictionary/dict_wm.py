#!/usr/bin/env python2
# -*- coding: utf-8 -*-  
import sys
import os
import urllib2
from bs4 import BeautifulSoup

dict_web = 'https://www.merriam-webster.com/dictionary/'

def show_text(text):
    text = os.linesep.join([s for s in text.splitlines() if s])   # remove empty lines
    #text = " ".join([s for s in text.splitlines() if s])   # join lines
    #text = " ".join(text.split()) # remove multiple spaces 
    print text

def show_objs(objs ):
    for obj in objs :
        if not obj.find('script') :
            show_text(obj.text)

def main():
    reload(sys)                         # 2
    sys.setdefaultencoding('utf-8')     # 3
    try:
        if len(sys.argv) == 2:
            word_lookup = sys.argv[1]
        else:
            print 'What do you want to look up?'
            sys.exit(1)

        page = urllib2.urlopen(dict_web + word_lookup)
        #result = f.read()
        soup = BeautifulSoup(page, 'html.parser')
        #print(soup.prettify())

        print '\n' + '\t \t' + word_lookup + '\n'  
        # pronunciation section
        print '*************************************'  
        text = soup.body.find('div', attrs={'class' : 'entry-attr'}).text
        text = os.linesep.join([s for s in text.splitlines() if s])   # remove empty lines
        text = " ".join(text.split()) # remove multiple spaces 
        print text

        # meaning section
        print '\n**********meaning******************'  
        objs = soup.find_all('div', attrs={'class' : 'vg'})
        show_objs(objs)

        # exsamples section
        print '\n**********examples*****************'  
        objs = soup.find_all('ol', attrs={'class' : 'definition-list no-count'})
        show_objs(objs)

    except AttributeError:
        print "word can not be found"
        sys.exit(2)

    except TypeError:
        print "NA"
 
if __name__ == '__main__':
    main()
