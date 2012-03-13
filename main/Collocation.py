'''
Created on Nov 26, 2011

@author: Daniel Kershaw
'''
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.corpus import stopwords

class Collocation(object):
    '''
    Class to all for collocations to be calculated and returned. 
    '''


    def __init__(self, pos):
        '''
        Constructor for the generation of collocation class.
        @param pos: POS tagged data which is going to be chunked.
        '''
        self.pos = pos
        self.stopset = set(stopwords.words('english'))
        self.filter_stop = lambda w: len(w) < 3 or w in self.stopset
        
    def col(self, text, tok):
        '''
        The Collocation method which created the Bi and Tri Gram collocations.
        
        @param text: The POS tagged text which is going to collocated
        @param tok: Tokkonized text which will be used to check that collocation
                    don't cross sentece boundrys.
                    
        @return: A collection of Tri andBi Collocations which dont cross sentece boundries.
        '''
        bi = self.BiGram(text)
        tri = self.TriGram(text)
        
        tmp = []
        
        for phrase in bi + tri:
            for sent in tok:
                count = 0
                for word in sent:
                    for pword in phrase:
                        if pword[0] == word:
                            count = count + 1
                            
                if count == len(phrase):
                    tmp.append(phrase)

                 
        return tmp
        
    def BiGram(self, text):
        '''
        @param text: pos tagged text, also tokkonized
        This use the NLTK Collocations methods to find the relevent collocations
        which have a frequancy of 1 or more
        @return: a pos lag list of list words in phrases.
        '''
        
        words = []
        for s in text:
            for w in s:
                words.append(w[0])

        bi = BigramCollocationFinder.from_words(words)
        bi.apply_word_filter(self.filter_stop)
        bi.apply_freq_filter(1)
        tmp = bi.nbest(BigramAssocMeasures.chi_sq, 20)
        
        tmp1 = []
        for word in tmp:
            tmp1.append(self.pos.POSTag(word, s=True))
        
        return tmp1
        
    def TriGram(self, text):
        '''
        @param text: POS tagged text which is going to be collocated.
        
        This use the NLTK Collocations methods to find the relevent collocations
        which have a frequancy of 1 or more
        
        @return: A set of Tri Gram Collocations.
        '''
        words = []
        for s in text:
            for w in s:
                words.append(w[0])
                
        tri = TrigramCollocationFinder.from_words(words)
        tri.apply_word_filter(self.filter_stop)
        tri.apply_freq_filter(1)
        tmp = tri.nbest(TrigramAssocMeasures.chi_sq, 20)
        
        tmp1 = []
        for word in tmp:
            tmp1.append(self.pos.POSTag(word, s=True))
        
        return tmp1

    def fullstopcheck(self, items):
        '''
        
        Removes collocations which words cross sentece boundry lines. This is done by comparing the 
        words with there positions in the Tokonized text. 
        
        @param items: The complete set of collocations.
        
        @return: A set of collocation.
        '''
        tmp = []
        for phrase in items:
            count = 0
            possition = 0
            for word in phrase:
                if word[0][-1] == '.':
                    word = word[:-1]
                    possition = count + 1
                count = count + 1
            if count == possition:
                tmp.append(phrase)
            elif possition == 0:
                tmp.append(phrase)
        
        return tmp
