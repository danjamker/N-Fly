'''
Created on Nov 24, 2011

@author: Daniel Kershaw
'''
import nltk
from nltk.tokenize import *

class Tokenize(object):
    '''
    Tokonize Class
    '''


    def __init__(self, Filter):
        '''
        Constructor inisiates filter. 
        '''
        self.FF = Filter
        
    def Tok(self, text):
        '''
        Method for tokoniziong raw text. 
        
        @param text: plaine text to be tokonized. 
        @return: list of Tokonized text.
        '''
        sentance = nltk.sent_tokenize(text)
        sentance = [WhitespaceTokenizer().tokenize(self.FF.strip(sent)) for sent in sentance]

        return sentance