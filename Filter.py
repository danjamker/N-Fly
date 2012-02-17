'''
Created on Nov 18, 2011

@author: Daniel Kershaw
'''
import re

class Filter(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def strip(self, text):
        tmp = self.punctuationRemove(text)
        tmp1 = self.numberRemove(tmp)
        return tmp1
        
    def punctuationRemove(self, text, regex='[^a-z0-9A-Z ]+'):
        return re.sub(regex, '', text)
    
    def numberRemove(self, text, regex = '\s(\s*[+-]?\s*(?:\d{1,3}(?:(,?)\d{3})?(?:\1\d{3})*(\.\d*)?|\.\d+)\s*)\s'):
        return re.sub(regex, ' ', text)
        