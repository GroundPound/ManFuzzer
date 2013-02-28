'''
Created on Dec 23, 2012

@author: Peter

This module contains a few functions for extracting the parameters out of a man page.
'''
import subprocess
import logging
from arguments.valuedarguments import ValuedArguments

TIMEOUT = 3

logger = logging.getLogger('man-fuzzer')



def mineflags(executable):
    '''Returns a set of progargs that can be used to generate arguments in a test case.'''
    # Mine the flags
    valuedarguments = ValuedArguments() 
    
    valuedarguments.parse(_mine_h_flags(executable,TIMEOUT))
    valuedarguments.parse(_mine_H_flags(executable,TIMEOUT))
    valuedarguments.parse(_mine_Help_flags(executable,TIMEOUT))
    valuedarguments.parse(_mine_Man_flags(executable,TIMEOUT))
    
    return valuedarguments

def _extract_arguments(command,timeout):
    try:
        child = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        child_output = child.communicate(timeout = timeout)
        return repr(child_output)        
    except Exception as e:
        logger.exception(e)
        return ""

def _mine_h_flags(executable,timeout):
    return _extract_arguments(str(executable) + " -h",timeout)

def _mine_H_flags(executable,timeout):
    return _extract_arguments(str(executable) + " -H",timeout)

def _mine_Help_flags(executable,timeout):
    return _extract_arguments(str(executable) + " --help",timeout)

def _mine_Man_flags(executable,timeout):
    return _extract_arguments("man " + str(executable),timeout)