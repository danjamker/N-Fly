'''
Created on Nov 22, 2011

@author: Daniel Kershaw
'''
from nltk.corpus import wordnet as wn

class WordNet(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    def commone(self, word1, word2):
        tmp1 = wn.synset(wn.synsets(word1)[0].name)
        tmp2 = wn.synset(wn.synsets(word2)[0].name)    
        tmp3 = tmp1.common_hypernyms(tmp2)
        return tmp3
    
    def compare(self, word1, word2):
        tmp1 = wn.synsets(word1)[0].name
        tmp2 = wn.synsets(word2)[0].name
        w1 = wn.synset(tmp1)
        w2 = wn.synset(tmp2)
        val = w1.wup_similarity(w2)
        return val