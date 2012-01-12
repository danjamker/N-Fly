'''
Created on Nov 19, 2011

@author: Daniel Kershaw
'''
import nltk
from Filter import Filter

def NGram(text, n=3):
    F = Filter()
    
    sentance = nltk.sent_tokenize(text)     
    sentance = [nltk.word_tokenize(F.strip(sent)) for sent in sentance]  
    sentence = [nltk.ngrams(sent, n) for sent in sentance]

    return sentence