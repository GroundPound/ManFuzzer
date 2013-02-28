'''
Created on Dec 28, 2012

@author: Peter

Parses and generates simple arguments.
'''

import re
import random

class SimpleArguments(object): 

    _SIMPLE_ARGUMENTS = '[\\s]\\-?\\-[\\w]+[\\w\\-]*'
    
    def __init__(self,parsetext=""):
        self.arguments = set()
        self.parse(parsetext)
        
    
    def parse(self,parsetext):
        matches = re.findall(self._SIMPLE_ARGUMENTS,parsetext)
        self.arguments |= {match.strip() for match in matches}
    
    def size(self):
        return len(self.arguments)
    
    def __str__(self, *args, **kwargs):
        return str(self.arguments)

    def genarg(self,value=None):
        '''
        value is unused for simple arguments.
        '''
        return random.sample(self.arguments, 1)[0]
        
    
    
    
        
        