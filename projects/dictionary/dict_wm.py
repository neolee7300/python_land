#!/usr/bin/env python2
# -*- coding: utf-8 -*-  
import sys, os, urllib2
from bs4 import BeautifulSoup

class Word_grabber:
    dict_web = 'https://www.merriam-webster.com/dictionary/'

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


def main():
    reload(sys)                         # 2
    sys.setdefaultencoding('utf-8')     # 3
    wg = Word_grabber('') 
    wg.show_text('web url is ' + wg.dict_web)

    try:
        if len(sys.argv) == 2:
            word_lookup = sys.argv[1]
        else:
            print 'What do you want to look up?'
            sys.exit(1)

        page = urllib2.urlopen(wg.dict_web + word_lookup)
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
        print '\n**********meaning******************'  
        objs = soup.find_all('div', attrs={'class' : 'vg'})
        wg.show_objs(objs)

        # exsamples section
        print '\n**********examples*****************'  
        objs = soup.find_all('ol', attrs={'class' : 'definition-list no-count'})
        wg.show_objs(objs)

    except AttributeError:
        print "word can not be found"
        sys.exit(2)

    except TypeError:
        print "NA"

if __name__ == '__main__':
    main()
