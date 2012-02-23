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
        
    def Grams(self, pos, n=3, boundy=1):
        '''
        
        '''
        ngrams = []
        for x in range(2, n):
            ngrams.append(self.Gram(pos, n=x))
            
#        for x in range(1, n-2):
#            for grams in ngrams[x]:
#                for g in ngrams[x-1]:
#                    tmp = set(grams) & set(g)
#                    if len(tmp) == len(g):
#                        try:
#                            ngrams.remove(g)
#                        except:
#                            pass
        
        tmp = []
        
        for x in range(0, n-2):
            tmp = tmp + ngrams[x]
        
        print "tmp is this, ", tmp
            
        return tmp
        
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
    
    def capitalList(self, text):
        '''
        
        
        @param text: text input which has to be 
        @return: List of tagged words which havve all capitalized first letters
        ''' 
        tmp = []
        
        for sent in text:
            count = 0
            for word in sent:
                if (word[0][0].isupper() & count == 0) | (word[0][0].islower() & count > 0):
                    t = []
                    for x in range(count, len(sent)):
                        if  sent[x][0][0].isupper():
                            t.append(sent[x])
                        else:
                            if len(t) >= 2:
                                tmp.append(t)
                                print "FOUND ONE: ", t
                            t = []
                            break
                    
                count = count + 1
                
        return tmp