'''
The main accessor class for project N-Fly.
This encapsulates all other methods in line the with FYP report.

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
    Class for selecting keywords and extracting keywords from online contentent.
    '''

    def __init__(self, llwl='Brown', llNL=2, percen=80, NE = True, Col = True, Gram = True, Chu = True):
        '''      
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
    
    def Select(self, url, depth): 
        '''
        Determin the best keywords for a webpage.
        
        @param url: the base url to start sampaling from
        @param depth: the depth of the website to be sampled
        
        @return: the list of selected keywords, ordered with the highest rated words to the lower bownd of array.
        '''     
        #Get data from web page
        text = self.GD.getWebPage(url, depth)

        #Tokonize sentance and words
        tok = self.To.Tok(text)

        #POS tag the text
        pos = self.POS.POSTag(tok, 'tok')

        #Log Likly Hood
        log = self.LL.calcualte(tok)
 
        #Collocations
        if self.Col == True:
            col = self.CC.col(pos, tok)
        else:
            col = []

        #NE Extraction
        if self.NEs == True:
            ne = self.Cu.Chunks(pos, nodes=['PERSON', 'ORGANIZATION', 'LOCATION'])
        else:
            ne = []
         
        #Extract NP
        if self.Chu == True:
            chu = [self.Cu.parse(p) for p in pos]
        else:
            chu = []
        
        #Creat N-gram 
        if self.Gram == True:
            ga = self.Ng.Grams(pos, n=6)
        else:
            ga = []
        
        return self.S.keywords(ne, ga , col , chu, log)

