'''
Created on Nov 15, 2011

@author: Daniel Kershaw
'''
from nltk.corpus.reader import WordListCorpusReader
from cPickle import load, dump
import os
import string
import nltk

class AmE06(object):
    '''
    Class for the AmE06 Wordlist corpora.
    '''

    def __init__(self):
        '''
        Constructor for the AmE06 word list corpa. 
        
        Initaly the contructor trys to load the corpora from a .plk file. If this has not
        created, then a new instance is created by iterating though all files for BE06.
        '''
        
        try:
            #Attempt to open .plk file and load. 
            input = open("./Corpus/AmE06/AmE06.pkl", 'rb')
            reader = load(input)
            input.close()
        except IOError as e:
            
            filelist = []
            words = []
            
            #Find all .txt files in /AmE06 dirctory
            for files in os.listdir("./Corpus/AmE06/"):
                if files.endswith(".txt"):
                    filelist.append(files)
            
                       
            if(len(filelist)== 500):
                
                #Iterate through whole list of file
                for name in filelist:
                    f = open("./Corpus/AmE06/" + name)
                
                    lines = f.readlines()
                    
                    #Read line in file, tokonize to words, and remove all 
                    #Punctuation
                    for line in lines:
                        tmp1 = nltk.sent_tokenize(line)
                        for lin in tmp1:
                            tmp = nltk.word_tokenize(lin)
                            for word in tmp:
                                for c in string.punctuation:
                                    word= word.replace(c,"")
                                words.append(word)
                            
                    f.close()
                
                #Write wordlist to output file.
                a = open("./Corpus/AmE06/finalcorpa.txt", "wb") 
                for word in words:
                    if word not in ".,;!?\"":
                        a.write(word + '\n')   
                        
                a.close()    
                
                #Creat NLTK corpus, and save a copy in folder for later use
                reader = WordListCorpusReader('./Corpus/AmE06', ['finalcorpa.txt'])
                output = open("./Corpus/AmE06/AmE06.pkl", 'wb')
                dump(reader, output, -1)
                output.close()
            else:
                reader = WordListCorpusReader('./Corpus/AmE06', ['finalcorpa.txt'])
                output = open("./Corpus/AmE06/AmE06.pkl", 'wb')
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