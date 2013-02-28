'''
Created on Dec 30, 2012

@author: Peter
'''
import random
import string

class DataValueGenerator(object):
    '''
    Generates random binary values.
    '''


    def __init__(self,meanlen,stdlen):
        self.meanlen = meanlen
        self.stdlen = stdlen
        
        
        
    def generate(self):
        length = max(0,int(random.gauss(self.meanlen, self.stdlen)))
        if length % 2 == 1:
            length += 1
        return "".join([random.choice(string.hexdigits) for _ in range(length)])
        
        