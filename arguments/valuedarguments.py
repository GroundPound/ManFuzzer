'''
Created on Dec 28, 2012

@author: Peter
'''

import re
import random
import logging
from arguments.simplearguments import SimpleArguments

class ValuedArguments(object):
    '''
    This argument class is for arguments whose values must be inserted with an = sign.
    
    Excerpt from ENV:
    
    
      -u NAME
      --unset=NAME
           Remove variable NAME from the environment, if it was in the
           environment.
           
    Here, --unset is considered a valued argument.
    '''
    
    _VALUED_ARGUMENTS = '[\\s]\\-\\-?[\\w]+[\\w\\-]*='
    logger = logging.getLogger('valued-arguments')


    def __init__(self,parsetext=""):
        self.valuedarguments = set()
        self.simplearguments = SimpleArguments(parsetext)
        self.parse(parsetext)
        
    def parse(self,parsetext):
        self.logger.debug("Parsing: " + parsetext)
        matches = re.findall(self._VALUED_ARGUMENTS,parsetext)
        self.valuedarguments |= {match.strip() for match in matches}
        self.simplearguments.parse(parsetext)
    
    def size(self):
        return len(self.valuedarguments) + self.simplearguments.size()
    
    def __str__(self, *args, **kwargs):
        return str(self.valuedarguments) + str(self.simplearguments)

    def genarg(self,value=None):
        '''
        If a string value is provided, then it will be added to an argument.
        '''        
        if value is None:
            return self.simplearguments.genarg()
        else:
            if random.randint(0,self.size()) < len(self.valuedarguments):
                return random.sample(self.valuedarguments, 1)[0] + value
            else:
                return self.simplearguments.genarg() + " " + value
    
    
    
    
    
    
    