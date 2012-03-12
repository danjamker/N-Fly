'''
Created on Dec 9, 2011

@author: Daniel Kershaw
'''
from nltk import *
from decimal import *
from phrase import phrase
from nltk.stem.wordnet import WordNetLemmatizer

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
        self.lmtzr = WordNetLemmatizer()
        
    def keywords(self, NE, Gram, Col, Chunk, log):
        '''
        This selects the most likly keyterms from potential candidates
        passed in. 
        
        @param NE: list of pos tagged Named Entities
        @param Gram: list of pos tagged n-grams
        @param Col: list of pos tagged collocations
        @param Chunk: list of pos tagged chunks 
        @param log: loglikly hood directory passed  
        
        @return: selected keywords. 
        '''
        self.log = log
        
        master = []
        
        fdist = FreqDist()
        for word in Gram + NE + Col + Chunk:
            if word:
                fdist.inc(tuple(word))
              
        for key in fdist.keys():
            if fdist[key] > 1:
                master.append(list(key))
                          
        input = filter(None, Gram + NE + Col + Chunk)
        tmplist = []    
        phrasearray = []     
        
        #Strips phrases which have stop words within them.
        for grams in input:
            
            boolean = False
            for word in grams:
                if word[0].lower() in self.stopwords:
                    boolean = True
            
            if grams[0][0] == "The":
                boolean = False 
            
            #If capital The at end of phrase then remove it form the word.
            if grams[-1][0] == "The":
                tmp = []
                for tupple in grams[:-1]:
                    tmp.append(tupple)
                grams = tuple(tmp)
               
            if (self.all_same(grams) == True) & (len(grams) > 1):
                boolean = True
                              
            if boolean == False:
                tmplist.append(grams)
        
        #parses the list into phrase objects
        for w in tmplist:
            phrasearray.append(phrase(w, tmplist, self.log))
            
        
        #Retrives there intercepts for each word. 
        intercepts = []
        for a in phrasearray:
            b = a.getSet()
            if b:
                intercepts.append(list(b))
             
        oneword = []
              
        for w in phrasearray:
            if w.getNumberCapitals() >= (w.getLength()):
                    oneword.append(w.getPhrase())
        
        ma = self.duplicates(oneword + intercepts)
        master = self.du(ma)
        master = self.lookforjoins(master)
        
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
        
       
        tmp1 = []
        for grams in tmp3:
            tmp1.append(' '.join(grams[0:-1]))
              
        #The number of items which is the x%                
        x = int(round(float(float(float(len(tmp1))/float(100))*self.percentil)))
        return tmp1[-x:]

        
    def bubbleSort(self, list):
        '''
        Bubble sort algorythm to sort nested list
        Sortbased on last value in each list
        
        @param list: list to sort 
        '''
        print len(list)
        swap_test = True
        while swap_test:
            swap_test = False
                
            for i in range(0, len(list) - 1):
                if list[i][-1] > list[i + 1][-1]:
                    list[i], list[i + 1] = list[i + 1], list[i]
                    swap_test = True
        print len(list)
        return list
    
    def bubbleSortLength(self, list):
        '''
        Bubble sort algorythm to sort nested list
        Sortbased on last value in each list
        
        @param list:list to sort 
        @return list of sorted words. 
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
        @return: list of ordered words. 
        '''
        # order preserving
        checked = []
        tmp = self.bubbleSortLength(seq)
        
        for phrase in tmp:
            tmplist = []
            for p in tmp:
                if len(set(phrase) & set(p)) > (round(float(len(phrase))/float(2))):
                    tmplist.append(p)
                    tmp.remove(p)
            
            t = set()
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
        '''
        Mothod to eliminate part duplicates
        
        @param input: list of potential keywords. 
        @return: list of keywords which have been selected. 
        '''
        
        tmp = []
                
        for phrase in input:
            boolean = True
            for p in tmp:
                if phrase == p:
                    boolean = False
            
            if boolean == True:
                tmp.append(phrase)

        for phrase in tmp:
            if len(phrase) >= 2:
                if phrase[0][0][0].islower():
                    phrase.remove(phrase[0])  
            
            if len(phrase) >= 2:
                if phrase[-1][0][0].islower():
                    phrase.remove(phrase[-1])  
                
        i = True
        while i == True: 
            i = False
            for phrase in tmp[:]:
                boolean = False                     
                
                for p in tmp:
                    if len(phrase) > len(p):
                        if len(set(phrase) & set(p)) == len(phrase)-1:
                            print phrase
                            print p
                            one = set(phrase) - (set(phrase) & set(p))
                            if list(one)[0][0].islower():
                                try:
                                    tmp.remove(phrase)
                                except:
                                    pass
                                i = True
                            else:
                                try:
                                    tmp.remove(p)
                                except:
                                    pass
                                
                                i = True


                            
            

        return tmp
    
    def all_same(self,items):
        '''
        @param items: list of keywords. 
        '''
        return all(x == items[0] for x in items)
    
    def du(self, items):
        '''
        Mothod to delete duplicates from list:
        
        @param items: List of keywords
        @return: list of keywords minus the duplicates. 
        '''
        seen = []
        for n in items:
            print n
            if not n in seen:
                seen.append(list(n))

        return seen
    
    def lookforjoins(self, items):
        '''
        Looking for join between words. 
        e.g. 'Apple Computer' and 'Computer Laptops' would become:
            Apple Computer Laptops
        
        @param items: The list of keywords
        @return: List of joined keywords. 
        '''
        newwordlist = []
        removewordlist = []
        for phrase in items:
            lastword = phrase[-1][0]
            #print "The last word is: ", lastword
            for p in items:
                if p != phrase:
                    #"The first word is: ", p[0][0]
                    if p[0][0] == lastword:
                        newword = phrase[:-1] + p
                        newwordlist.append(newword)
                        removewordlist.append(phrase)
                        removewordlist.append(p)
                                                
        for phrase in removewordlist:
            print phrase
            try:
                items.remove(phrase)
            except:
                pass
            
        return items + newwordlist