'''
Created on Dec 6, 2011

@author: Daniel Kershaw
'''
from Filter import Filter
import nltk

class NGram(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.F = Filter()
    
    def Gram(self, text, n=3, boundy=1):
        '''
        
        @param text: text to be created into Ngrams
        @param n: Length of Ngrams
        @param boundy: Number of instiances of gram
           
        @return: List of ngrams of text
        '''
        
        sentence = [nltk.ngrams(sent, n) for sent in text]
        t = []
        for s in sentence:
            t = t + s
            
        freq = nltk.FreqDist(t)
        
        tmp = []
        for f in freq.keys():
            if int(freq[f]) > boundy:
                tmp.append(f)
            
        return tmp
    
    def NGramUn(self, text, n=3):

        sentance = nltk.sent_tokenize(text)     
        sentance = [nltk.word_tokenize(self.F.strip(sent)) for sent in sentance]  
        sentence = [nltk.ngrams(sent, n) for sent in sentance]
    
        return sentence
