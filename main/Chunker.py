'''
Created on Nov 17, 2011

@author: Daniel Kershaw

Class which contains all the methods for the Chunking modual.
This allows for the extractions of phrases though either a trained method of RegEx matching. 
'''
from nltk.chunk import RegexpParser
from nltk.chunk.util import conlltags2tree
from nltk.chunk.util import tree2conlltags
from nltk.corpus import conll2000
import nltk

class Chunker(object):
    '''
    Class for Chunking using NLTK methods. 
    '''

    def __init__(self, POS):
        '''      
        @param POS: the POS tagger is passed through 
        '''
        train_sents = conll2000.chunked_sents()
        train_data = [[(t, c) for w, t, c in tree2conlltags(sent)]
                      for sent in train_sents]
        self.T = nltk.TrigramTagger(train_data)
        self.Tagger = POS
        self.tmp = []
    
    def Chunks(self, text, nodes):
        '''
        Main accessor method, masks the joining of methods.
        
        @param text: The text to be chunked.
        @param nodes: Which nodes to look for.   
        '''
        tmp = []
        for n in nodes:
            tmp = tmp + self.NE(text, node=n)
            
        return tmp
    
    def Chunk(self, sentence, node='NP', grammer=r"""
                  NP: {<DT|PP\$>?<JJ>*<NN>}
                      {<NNP>+}
                      """):
        '''
        Takes text and returns a list of noune and noun phrases, this is done
        by a form RegEx matching which is included in the NLTK libary.
    
        @param text: the text that is going to be chunked
        @param node='NP': this is which node to chunk 
        @param grammer='NP: {<DT|PP\$>?<JJ>*<NN>}{<NNP>+}': the grammar ReGex to use for chunking 
        
        @return: A nested list of tuples of chunked phrases with pos tagging.
        '''

        tmp = []

        cp = RegexpParser(grammer)
             
        for sent in sentence:
            for phrase in self.sub_leaves(cp.parse(sent), node):
                tmp.append(phrase)

        results = []
        for phrase in tmp:
            string = ""
            for (word, tag) in phrase:
                string = string + word + " "
            
            results.append(string[:-1])
            
        return results
    
    def parse(self, sentence):
        '''
        Constructs a parse tree out of the POS tagged data. 
        The tree is then scaled looking for Noun Phrases, which are then
        returned in a list.

        @param sentence: the chunked sentace to be parsed
        
        @return: list tagged words which where tagged NP
        '''
        pos_tags = [pos for (word, pos) in sentence]
        tagged_pos_tags = self.T.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        colltags = [(word, pos, chunktag) for ((word, pos), chunktag)
                    in zip(sentence, chunktags)]
        
        tmp = []
        tmp1 = []
        for (w, p, i) in colltags:
            if i == 'B-NP':
                tmp1.append((w, p))
            elif i == 'I-NP':
                tmp1.append((w, p))
            else:
                if tmp1:
                    tmp.append(tmp1)
                    tmp1 = []

        if tmp:
            t = filter(None, tmp[0])
            return t
    
    def NE(self, text, node='PERSON'):
        '''
        Named Entity Recognition Modual
        
        Creats a tree with the tags bellow, and extracts phrases which are tagged
        with the tagged what has been selected. 
        
        @param text: The text to return nodes form
        @param node: Name of nodes to be returned
       
        
        @note:  Can only be: ORGANIZATION, PERSON, LOCATION, DATE, TIME, MONEY, PERCENT, FACILITY, GPE 
  
        @return: List of List tagged phrases and words
        which come from a node of the node passed
        '''
        tmp = []
        
        for sent in text:
            for phrase in self.sub_leaves(nltk.ne_chunk(sent), node):
                tmp.append(phrase)
            
        return tmp
            
    def sub_leaves(self, tree, node):
        '''
        Returns a list of sub-leaves depending on there tags
        
        @param tree: the chunked tree going to be searcher
        @param node: which node to look for 
        
        @return: list of list of tuples  
        '''
        return [t.leaves() for t in tree.subtrees (lambda s: s.node == node)]
