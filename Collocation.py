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
    classdocs
    '''


    def __init__(self, pos):
        '''
        Constructor
        
        @param pos: 
        
        '''
        self.pos = pos
        self.stopset = set(stopwords.words('english'))
        self.filter_stop = lambda w: len(w) < 3 or w in self.stopset
        
    def BiGram(self, text):
        '''
        @param text: pos tagged text, also tokkonized
        
        This use the NLTK Collocations methods to fnid the relevent collocations
        which have a frequancy of 1 or more 
        
        @return: a pos lag list of list words in phrases.
        '''
        #change input to pos tagged and remove the tagging at the end. 
        #this would then mean this nested loop does not need changing, 
        
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
        
        return self.fullstopcheck(tmp1)
        
    def TriGram(self, text):
        '''
        
        @param text:
        
        @return:  
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
        
        return self.fullstopcheck(tmp1)

    def fullstopcheck(self, items):
        tmp = []
        for phrase in items:
            count = 0
            possition = 0
            for word in phrase:
                if word[0][-1] == '.':
                    print "Fonud a stop", phrase
                    word = word[:-1]
                    possition = count + 1
                count = count + 1
            print "Count and positoin", count, " ", possition
            if count == possition:
                tmp.append(phrase)
            elif possition == 0:
                tmp.append(phrase)
        
        print "Collocations removing of full stops", tmp
        return tmp
