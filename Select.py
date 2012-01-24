'''
Created on Dec 9, 2011

@author: Daniel Kershaw
'''
from nltk import corpus
from decimal import *
from phrase import phrase

class Select(object):
    '''
    Class used to select the relevent keyterms for the ouput. 
    This is down through first looking for part of duplicates
    looking to see if they comply with the rules, and one is 
    either deleted or both kept. 
    
    Then the list is ordered on there avrage log likley hood for 
    all the words in the phrase
    
    @todo: impliment phusdo code
    '''


    def __init__(self, percentil = 20):
        '''
        Inisalises the stop word list and sets the precisions
        of the out put. 
        
        @param percentil: default = 20 
        '''
        getcontext().prec = 2
        self.percentil = percentil
        self.stopwords = corpus.stopwords.words('english')
        self.stopwords.append('said')
        
    def keywords(self, NE, Gram, Col, Chunk, log):
        '''
        This selects the most likly keyterms from potential candidates
        passed in. 
        
        @param NE: list of pos tagged Named Entities
        @param Gram: list of pos tagged n-grams
        @param Col: list of pos tagged collocations
        @param Chunk: list of pos tagged chunks 
        @param log: loglikly hood directory passed  
        '''
        input = filter(None, NE + Gram + Col + Chunk)
        tmplist = []    
        phrasearray = []     
        
        #Strips phrases which have stop words within them.
        for grams in input:
            
            boolean = False
            for word in grams:
                if word[0].lower() in self.stopwords:
                    boolean = True
                               
            if boolean == False:
                tmplist.append(grams)
        
        #parses the list into phrase objects
        for w in tmplist:
            phrasearray.append(phrase(w, tmplist, log))
        
        #Retrives there intercepts for each word. 
        intercepts = []
        for a in phrasearray:
            b = a.getSet()
            if not b:
                print "None"
            else:
                intercepts.append(list(b))
             
        oneword = []
              
        for w in phrasearray:
            if w.getLength() == w.getNumberCapitals():
                    oneword.append(w.getPhrase())
        
        master = self.f2(self.duplicates(oneword + intercepts))
        
        tmp1 = []
        for grams in master:
            tmp = []
            avrage = 0
            i = 0
            for words in grams:
                tmp.append(words[0])
                try:
                    avrage = avrage + log[words[0].lower()]
                except:
                    avrage = avrage + 0
                i = i + 1
            try:
                avrage = avrage / i
            except:
                avrage = 0
            tmp.append(avrage)
            tmp1.append(tmp)            
        
        tmp3 = self.bubbleSort(tmp1)
        
        print tmp3
        
        tmp1 = []
        for grams in self.duplicates(tmp3):
            tmp1.append(' '.join(grams[0:-1]))
              
        #The number of items which is the x%                
        x = int(round(float(float(float(len(tmp1))/float(100))*self.percentil)))

        return tmp1[-x:]
        
    def bubbleSort(self, list):
        '''
        Bubble sort algorythm to sort nested list
        Sortbased on last value in each list
        
        @param list to sort 
        '''
        swap_test = True
        while swap_test:
            swap_test = False
                
            for i in range(0, len(list) - 1):
                if list[i][-1] > list[i + 1][-1]:
                    list[i], list[i + 1] = list[i + 1], list[i]
                    swap_test = True
        return list
    
    def bubbleSortLength(self, list):
        '''
        Bubble sort algorythm to sort nested list
        Sortbased on last value in each list
        
        @param list to sort 
        '''
        swap_test = True
        while swap_test:
            swap_test = False
                
            for i in range(0, len(list) - 1):
                if len(list[i]) < len(list[i + 1]):
                    list[i], list[i + 1] = list[i + 1], list[i]
                    swap_test = True
        return list

    def f2(self,seq): 
        '''
        Checks a list for diplicate items
        
        @param seq the list to be run through: 
        '''
        # order preserving
        checked = []
        tmp = self.bubbleSortLength(seq)
        print tmp 
        
        for phrase in tmp:
            tmplist = []
            for p in tmp:
                if len(set(phrase) & set(p)) > (len(phrase)/2):
                    tmplist.append(p)
                    tmp.remove(p)
            
            t = set(tmplist[0])
            for word in tmplist:
                t = set(t) & set (word)
            
            wt = []
            for words in phrase:
                for w in list(t):
                    if w == words:
                        wt.append(words)
                            
            checked.append(wt)                  
        
        return checked + tmp
    
    def duplicates(self, input):
        
        tmp = []
                
        for phrase in input:
            boolean = True
            for p in tmp:
                if phrase == p:
                    boolean = False
            
            if boolean == True:
                tmp.append(phrase)
                
        return tmp
        