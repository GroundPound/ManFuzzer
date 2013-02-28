'''
Created on Dec 30, 2012

@author: Peter
'''
import tempfile
import os
import binascii
import logging
from values.datagen import DataValueGenerator


class FileValueGenerator(object):
    '''
    Generates random files.
    '''

    logger = logging.getLogger('filegen')

    def __init__(self,meanlen,stdlen):
        self.meanlen = meanlen
        self.stdlen = stdlen
        
        
        
    def generate(self):
        dvg = DataValueGenerator(self.meanlen, self.stdlen)
        data = dvg.generate()
        fp = tempfile.NamedTemporaryFile(delete=False)
        fp.write(binascii.a2b_hex(data))        
        fp.close()
        self.logger.debug("Temp file name: %s " % fp.name)
        return '"' + os.path.abspath(fp.name) + '"'
        
        
        
