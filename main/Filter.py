'''
Created on Nov 18, 2011

@author: Daniel Kershaw
'''
import re

class Filter(object):
    '''
    Filter class for removing elements from strings.
    '''

    def __init__(self):
        '''
        '''
    
    def strip(self, text):
        '''
        Filters the text first with a punctuation filter, and then with a number 
        filter
        
        @param  text: The Sentence which is going to be filtered.
        
        @return: the sentecte with the elements removed.
        '''
        tmp = self.punctuationRemove(text)
        tmp1 = self.numberRemove(tmp)
        return tmp1
        
    def punctuationRemove(self, text, regex='[^a-z0-9A-Z -]+'):
        '''
        For filtering punctuation from the punctuation.
        
        @param text: the String which is going to be filtered
        @param regex: the regex which is going to be used for filtering. 
        '''
        return re.sub(regex, ' ', text)
    
    def numberRemove(self, text, regex = '\s(\s*[+-]?\s*(?:\d{1,3}(?:(,?)\d{3})?(?:\1\d{3})*(\.\d*)?|\.\d+)\s*)\s'):
        '''
        For filtering nunbers from the punctuation.
        
        @param text: the String which is going to be filtered
        @param regex: the regex which is going to be used for filtering. 
        '''
        return re.sub(regex, ' ', text)
        