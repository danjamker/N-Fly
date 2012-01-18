'''
Created on Nov 20, 2011

@author: Daniel Kershaw
'''

class Stats(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    
    def weight(self, text, tags = ['NNS', 'NN', 'NNP', 'NNPS', 'NN-TL', 'NP-TL']):
        tmp = []
        print text
        for l in text:
            for grams in l:
                score = 0
                for (word, tag) in grams:
                    for t in tags:
                        if tag == t:
                            score = score + 1
                tmp.append([grams, score])
        
        return tmp[::-1] 