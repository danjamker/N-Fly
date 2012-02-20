'''
Created on Nov 24, 2011

@author: Daniel Kershaw
'''
import nltk
from nltk.tokenize import *

class Tokenize(object):
    '''
    classdocs
    '''


    def __init__(self, Filter):
        '''
        Constructor
        '''
        self.FF = Filter
        
    def Tok(self, text):
        sentance = nltk.sent_tokenize(text)
        sentance = [WhitespaceTokenizer().tokenize(self.FF.strip(sent)) for sent in sentance]
        #for s in sentance:
        #    for w in s:
        #        if w[-1] == ".":
        #            print "Removing full stop", w
        #            w = w[:-1]
        return sentance