'''
Created on 29 Dec 2011

@author: Daniel Kershaw
'''

class phrase(object):
    '''
    classdocs
    '''

    def __init__(self, phrase, text, log):
        '''
        @param phrase: The particular phrase this class is for. 
        @param text: List of all words
        @param log: loglikly hood directory   
        '''
        self.phrase = phrase
        self.length = len(phrase)
        
        
        self.similarPhrase = []
        
        for other_phrase in text:
                if other_phrase != phrase:
                    a = set(phrase)
                    b = set(other_phrase)
                    if(len(a&b) > (len(a)-1) ):
                        self.similarPhrase.append(other_phrase)
        
        self.avLog = 0
        for word in phrase:
            self.avLog = self.avLog + log[word[0].lower()]
        try:
            self.avLog = self.avLog / self.length
        except:
            self.avLog = 0
        
        self.numCap = 0
        for word in phrase:
            if word[0][0].isupper():
                self.numCap = self.numCap + 1
        
        self.numNouns = 0
        for word in phrase:
            if word[1] in ['NN','NN$','NNS','NNS$','NP','NP$','NP$','NPS$','NR']:
                self.numNouns = self.numNouns + 1
        
        self.type = "tmp"
        tmp = None
        t =[]
        if len(self.similarPhrase) != 0:
            tmp = phrase
            for w in self.similarPhrase:
                tmp = set(tmp) & set(w)
        
            
            
            for w in phrase:
                for b in tmp:
                    if w == b:
                        t.append(b)
        
        self.set = t
        print "-----------"
        print "Intercectio"
        print t
        print "List of smilar words"
        print self.similarPhrase
        print phrase
    def getPhrase(self, tag = True):
        '''
        @param tag: return with or without tags default True
        @@return list of words in phrase 
        '''
        if tag == True:
            return self.phrase
        elif tag == False:
            return None

    def getLength(self):
        '''
        @return: Length of phrase
        '''
        return self.length
    
    def getSimilarPhrases(self, number = 1):
        '''
        @param number: number of words similar which to return
                        default 1
        
        @return: List of similar phrase
        '''
        return self.similarPhrase
    
    def getArvageLog(self):
        '''
        @return: The avrage log for the phrase
        '''
        return self.avLog
    
    def getNumberNouns(self):
        '''
        @return: The number of nouns in the phrase
        '''
        return self.numNouns
    
    def getNumberCapitals(self):
        '''
        @return: Number of capitalized words
        '''
        return self.numCap
    
    def getSet(self):
        '''
        @return: Intersection of all simiar words
        '''
        return self.set