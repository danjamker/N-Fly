'''
Created on Nov 16, 2011

@author: Daniel Kershaw

Modual for the implimentation of LogLikelihood calculations. 
'''
import nltk
import math
from NGram import NGram
from BE06 import BE06
from AmE06 import AmE06
from decimal import *

class LogLikelihood(object):
    '''
    Class for creating an instanse of LogLilyHood
    '''

    def __init__(self, wordlist='Brown', NLength=2, prec=50):
        '''
        Inisiates the class, populating the frequancy data structures.
        @param wordlist: This is for which master corpus to use defaultis Brown
        @note: Posibal input - 
                Brown
                AmE06
                BE06
        @param NLength: of Ngrams to calculate log for default 2
        @param prec: the prossision of the log calculation 
        '''
        ng = NGram()
        getcontext().prec = prec

        if wordlist == 'Brown':
            self.fdist2 = nltk.FreqDist(nltk.corpus.brown.words())
            self.fdist2Gram = nltk.FreqDist(ng.NGramUn(nltk.corpus.brown.raw(), n=NLength)[0])
        elif wordlist == 'AmE06':
            self.fdist2 = nltk.FreqDist(AmE06().getCorpa().words())
            self.fdist2Gram = nltk.FreqDist(ng.NGramUn(AmE06().getCorpa().raw(), n=NLength)[0])
        elif wordlist == 'BE06':
            self.fdist2 = nltk.FreqDist(BE06().getCorpa().words())
            self.fdist2Gram = nltk.FreqDist(ng.NGramUn(BE06().getCorpa().raw(), n=NLength)[0])
        return
        
    def calcualte(self, text):
        '''
        Method to create a directory of log number based on input text
        
        @param text: the tockonised text which is going to have logs made of
        @return: a directory of log numbers to text in text input
        '''
        words = []
        for s in text:
            for w in s:
                words.append(w.lower())
        fdist1 = nltk.FreqDist(words)
        total1 = 0
        total2 = 0
        total = {}
        ll = total.copy()
        lll1 = []
        lll2 = []
        for k,v in fdist1.items():
            total[k] = ''
            total1 = total1 + v

        for k,v in self.fdist2.items():
            total[k] = ''
            total2 = total2 + v
            
        for k,v in total.items():
            x = fdist1.get(k)
            if x == None:
                x = 0
                
            y = self.fdist2.get(k)
            if y == None:
                y = 0
                        
            total[k] = x+y 
                 
        for k,v in fdist1.items():
            
            a = fdist1.get(k)
            if a == None:
                a = 0
                                
            b = self.fdist2.get(k)
            if b == None:
                b = 0
            
            c = total1
            d = total2
            
            try:
                E1 = float(c)*((float(a)+float(b))/(float(c)+float(d)))
            except:
                E1 = 0
                
            try:
                E2 = float(d)*((float(a)+float(b))/(float(c)+float(d)))
            except:
                E2 = 0
            
            try:
                aE1 = math.log(a/E1)
            except:
                aE1 = 0
                
            try:
                bE2 = math.log(b/E2)
            except:
                bE2 = 0
            
            try:
                lll1.append(k)
                lll2.append(float(2*((a*aE1)+(b*bE2))))
                ll[k] = 2*((a*aE1)+(b*bE2))
            except:
                lll1.append(k)
                lll2.append(0)
                ll[k] = 0
                       
        return ll
          
    def NGramLog(self, text):
        '''
        Method to create a directory of log number based on input text n-grams
        
        @param text: the tockonized text which is going to have logs made of
        @return: a directory of log numbers to text in text input n-grams
        '''
        fdist1 = nltk.FreqDist(text[0])
        total1 = 0
        total2 = 0
        total = {}
        ll = total.copy()
        lll1 = []
        lll2 = []
        for k,v in fdist1.items():
            total[k] = ''
            total1 = total1 + v

        for k,v in self.fdist2Gram.items():
            total[k] = ''
            total2 = total2 + v
            
        for k,v in total.items():
            x = fdist1.get(k)
            if x == None:
                x = 0
                
            y = self.fdist2Gram.get(k)
            if y == None:
                y = 0
                        
            total[k] = x+y 
                 
        for k,v in fdist1.items():
            
            a = fdist1.get(k)
            if a == None:
                a = 0
                                
            b = self.fdist2Gram.get(k)
            if b == None:
                b = 0
            
            c = total1
            d = total2
            
            try:
                E1 = float(c)*((float(a)+float(b))/(float(c)+float(d)))
            except:
                E1 = 0
                
            try:
                E2 = float(d)*((float(a)+float(b))/(float(c)+float(d)))
            except:
                E2 = 0
            
            try:
                aE1 = math.log(a/E1)
            except:
                aE1 = 0
                
            try:
                bE2 = math.log(b/E2)
            except:
                bE2 = 0
            
            try:
                lll1.append(k)
                lll2.append(float(2*((a*aE1)+(b*bE2))))
                ll[k] = 2*((a*aE1)+(b*bE2))
            except:
                lll1.append(k)
                lll2.append(0)
                ll[k] = 0
               
        return sorted(ll.items(), key=lambda x: x[1])[len(ll)-50: len(ll)]
    