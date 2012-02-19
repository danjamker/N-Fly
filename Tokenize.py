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
        sentance = [WhitespaceTokenizer().tokenize(sent) for sent in sentance]
        return sentance