'''
Created on Nov 17, 2011

@author: Daniel Kershaw
'''
from Filter import Filter
from cPickle import load, dump
import nltk

class POS(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''   
        self.FF = Filter()
        
        try:
            #Attempt to open .plk file and load. 
            input = open(".\\Corpus\\Brown-Uni.pkl", 'rb')
            self.unigram_tagger = load(input)
            input.close()  
        except IOError as e:   
            self.brown_tagged_sents = nltk.corpus.brown.tagged_sents(simplify_tags=False)
            t0 = nltk.DefaultTagger('NN')
            t1 = nltk.UnigramTagger(self.brown_tagged_sents, backoff=t0)
            t2 = nltk.BigramTagger(self.brown_tagged_sents, backoff=t1)
            self.unigram_tagger = nltk.UnigramTagger(self.brown_tagged_sents, backoff=t2)
            
            output = open(".\\Corpus\\Brown-Uni.pkl", 'wb')
            dump(self.unigram_tagger, output, -1)
            output.close()
    
    def POSTag(self, text, s='false'):
        '''
        
        @param text:
        @param s:
        
        @return: POSTaged version of input  
        '''
        if s == 'false':
            sentance = nltk.sent_tokenize(text)
            sentance = [nltk.word_tokenize(self.FF.strip(sent)) for sent in sentance]
            sentance = [self.unigram_tagger.tag(sent) for sent in sentance]
        elif s == 'tok':
            sentance = [self.unigram_tagger.tag(sent,) for sent in text]
        else:
            sentance = self.unigram_tagger.tag(text)
        
        
        return sentance
    
    def POSNgram(self, text, s='false', n=3):
        '''
        
        @param text: ngrams to be POS tagged
        @param s: 
        @param n: length of n gram  
        
        @return: OPSTagged Ngrams 
        '''
        if s == 'false':
            sentance = self.POSTag(text);
            sentence = [nltk.ngrams(sent, n) for sent in sentance]
        else:
            sentence = [nltk.ngrams(sent, n) for sent in text]
        
        return sentence

