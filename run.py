'''
Created on Nov 24, 2011

@author: Daniel Kershaw
'''
from Chunker import Chunker
from Collocation import Collocation
from Filter import Filter
from GetData import GetData
from LogLikelihood import LogLikelihood
from NGram import NGram
from POS import POS
from Select import Select 
from Tokenize import Tokenize

class runable(object):
    '''
    Class for selecting keywords
    '''

    def __init__(self, llwl='Brown', llNL=2, percen=100, NE = True, Col = True, Gram = True, Chu = True):
        '''
        Constructor
        
        @param llwl:LogLikleyHood Corpa name ('Brown','AmE06','BE06')
        @param llNL:LogLikleyHood 
        @param percen: Presision of output default = 20, 20% returned
        @param NE: Uses NE default True 
        @param Col: Uses Collocation default True
        @param Gram: Uses N-Grams default True
        @param Chu: Uses Chunking default True
           
        '''

        self.NEs = NE
        self.Col = Col
        self.Gram = Gram
        self.Chu = Chu
        self.p = percen
        print 'Starting to build ', llwl
        self.LL = LogLikelihood(wordlist=llwl, NLength=llNL)
        print 'LL Loaded'
        self.POS = POS()
        print 'POS Loaded'
        self.GD = GetData()
        print 'GD Loaded'
        self.Cu = Chunker(self.POS)
        print 'Cu Loaded'
        self.FL = Filter()
        print 'FL Loaded'
        self.CC = Collocation(self.POS)
        print 'CC Loaded'
        self.Ng = NGram()
        print 'Ng Loaded'
        self.S = Select(percentil=self.p)
        print 'S Loaded'
        self.To = Tokenize(self.FL)
        print 'To Loaded'
    
    def run(self, url, depth): 
        '''
        To determin the best keywords for a webpage
        
        @param url: the base url to start sampaling from
        @param depth: the depth of the website to be sampled
        
        @return: the list of selected keywords  
        '''     
        #Get data from web page
        text = self.GD.getWebPage(url, depth)
        
        #Tokonize sentance and words
        tok = self.To.Tok(text)
        print tok
        #POS tag the text
        pos = self.POS.POSTag(tok, 'tok')
        
        #Log Likly Hood
        log = self.LL.calcualte(tok)
        
        #Collocations
        if self.Col == True:
            Tcol = self.CC.TriGram(pos)
            Bcol = self.CC.BiGram(pos)
        else:
            Tcol = []
            Bcol = []

        #NE Extraction
        if self.NEs == True:
            person = self.Cu.NE(pos)
            orginisation = self.Cu.NE(pos, node='ORGANIZATION')
            location = self.Cu.NE(pos, node='LOCATION')
        else:
            person = []
            orginisation = []
            location = []
            
        #Extract NP
        if self.Chu == True:
            chu = [self.Cu.parse(p) for p in pos]
        else:
            chu = []
        
        #Creat N-gram 
        if self.Gram == True:
            g2 = self.Ng.Gram(pos, n=2)
            g3 = self.Ng.Gram(pos, n=3)
            g4 = self.Ng.Gram(pos, n=4)
            g5 = self.Ng.Gram(pos, n=5)           
            g6 = self.Ng.Gram(pos, n=6)
            #cap = self.Ng.capitalList(pos)   
                     
            ga = g2 + g3 + g4 + g5 + g6
        else:
            ga = []
        
        return self.S.keywords(person + orginisation + location, ga , Tcol + Bcol , chu, log)

