'''
Created on Nov 15, 2011

@author: Daniel Kershaw

Generates the BE06 wordlist Corpora from text fails or from a memory object.
@copyright: Paul Baker
'''
from cPickle import load, dump
from nltk.corpus.reader import WordListCorpusReader
import nltk
import os
import string

class BE06(object):
    '''
    Class for the BE06 Wordlist corpora construction and encapsulation.
    '''

    def __init__(self):
        '''
        Constructor for the BE06 word list corpa. 
        
        @note: Initaly the contructor tries to load the corpora from a .plk file. If this has not
        created, then a new instance is created by iterating though all files for BE06.
        '''
        
        try:
            #Attempt to open .plk file and load. 
            input = open("./Corpus/BE06/BE06.pkl", 'rb')
            reader = load(input)
            input.close()
        except IOError as e:
            filelist = []
            words = []
            
            #Find all .txt files in /BE06 dirctory
            for files in os.listdir("./Corpus/BE06"):
                if files.endswith(".txt"):
                    filelist.append(files)
            
            if(len(filelist) == 500):
                #Iterate through whole list of file
                for name in filelist:
                    f = open("./Corpus/BE06/" + name)
                
                    lines = f.readlines()
                    
                    #Read line in file, tokonize to words, and remove all 
                    #Punctuation
                    for line in lines:
                        tmp1 = nltk.sent_tokenize(line)
                        for lin in tmp1:
                            tmp = nltk.word_tokenize(lin)
                            for word in tmp:
                                for c in string.punctuation:
                                    word = word.replace(c, "")
                                words.append(word)
                            
                    f.close()
                
                #Write wordlist to output file.
                a = open("./Corpus/BE06/finalcorpa.txt", "wb") 
                for word in words:
                    if word not in ".,;!?\"":
                        a.write(word + '\n')   
                        
                a.close()    
                
                #Creat NLTK corpus, and save a copy in folder for later use
                reader = WordListCorpusReader('./Corpus/BE06', ['finalcorpa.txt'])
                output = open("./Corpus/BE06/BE06.pkl", 'wb')
                dump(reader, output, -1)
                output.close()
            else:
                reader = WordListCorpusReader('./Corpus/BE06', ['finalcorpa.txt'])
                output = open("./Corpus/BE06/BE06.pkl", 'wb')
                dump(reader, output, -1)
                output.close()
        
        #Return corpus
        self.corpa = reader
        
    def getCorpa(self):
        '''
        Getter to return instance of the Wrodlist Copora
        
        @return: BE06 Corpora
        '''
        return self.corpa
