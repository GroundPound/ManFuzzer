'''
Created on Dec 28, 2012

@author: Peter
'''
import random
import string

class TextValueGenerator(object):
    '''
    Generates random text.
    '''


    def __init__(self,meanlen,stdlen):
        self.meanlen = meanlen
        self.stdlen = stdlen
        
        
        
    def generate(self):
        length = max(0,int(random.gauss(self.meanlen, self.stdlen)))
        return '"' + "".join([random.choice(string.ascii_letters + string.digits) for _ in range(length)]) + '"'
        
        