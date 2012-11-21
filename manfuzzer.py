'''   Copyright 2012 Peter Chapman

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

The Man Fuzzer: Given a binary path this file produces parameter inputs to 
that binary based on the flags found in -h,-H,--help and the man page.'''

import argparse
import logging
import random
import subprocess
import sys
import re

MAGIC_REGEX = '[\\s]\\-?\\-[\\w\\-]+'
DEFAULT_TEST_CASES = 1000
AVERAGE_PARAMETERS = 1
STDDEV_PARAMETERS = 2

def main():
    parser = argparse.ArgumentParser(description='Produces command-line inputs to an executable for fuzzing based on the flags found by running -h, -H, --help, and the man page.')
    parser.add_argument('-d','--debug',help="Enables debugging output.",action="store_true")
    parser.add_argument('executable', help='The relative or absolute path to the executable to be fuzzed.')
    parser.add_argument('-c','--combinations', type=int,
                       default=DEFAULT_TEST_CASES,
                       help='The number of test cases to generate. The default is %d' % DEFAULT_TEST_CASES)
    parser.add_argument('-o','--outfile',
                       help='The file to which the test cases should be printed out. Each test case is separated by a new line character.')
    parser.add_argument('-m','--mean',help='The mean number of parameters to include in the test cases.',default=AVERAGE_PARAMETERS)
    parser.add_argument('-s','--stddev',help='The standard deviation number of parameters to include in the test cases.',default=STDDEV_PARAMETERS)
    args = parser.parse_args()
    debug = args.debug
    executable = args.executable
    combinations = args.combinations
    outputfile = args.outfile
    stddev = args.stddev
    average = args.mean
    logging.basicConfig(level=logging.DEBUG)
    logging.StreamHandler(sys.stderr)
    logger = logging.getLogger('man-fuzzer')
    
    if debug == True:
        logger.setLevel(logging.DEBUG)
        logger.info("Debug output is enabled.")        
    else:
        logger.setLevel(logging.WARNING)
        
    
    
    logger.info("Executable path: %s" % str(executable))

    
    # Mine the flags
    hFlags = mine_h_flags(executable)
    HFlags = mine_H_flags(executable)
    helpFlags = mine_Help_flags(executable)
    manFlags = mine_Man_flags(executable)

    flags = hFlags | HFlags | helpFlags | manFlags # union everything together

    test_cases = set() # a set of sets for each test case (to remove repeated trials)

    for _ in range(combinations):
        num_flags_used = int(random.gauss(average,stddev))
        num_flags_used = max(0,min(num_flags_used,len(flags)))
        test_case = frozenset(random.sample(flags,num_flags_used)) # created a test case!
        test_cases.add(test_case)
        
    output_string = '\n'.join([' '.join(test_case) for test_case in test_cases])
    
    if outputfile != None:
        with open(str(outputfile),'w') as outputfh:
            outputfh.write(output_string)
        
    else:
        print(output_string)

    logging.info("Exiting.")


def extract_arguments(command):
    try:
        child = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        child_output = child.communicate()
        logging.debug(child_output)
        matches = re.findall(MAGIC_REGEX,repr(child_output))
        return {match.strip() for match in matches}
    except:
        logging.error("Command failed: %s" % str(command))
        return set()

def mine_h_flags(executable):
    logging.info("Running -h")
    return extract_arguments(str(executable) + " -h")

def mine_H_flags(executable):
    logging.info("Running -H")
    return extract_arguments(str(executable) + " -H")

def mine_Help_flags(executable):
    logging.info("Running --help")
    return extract_arguments(str(executable) + " --help")

def mine_Man_flags(executable):
    logging.info("Finding man page")
    return extract_arguments("man " + str(executable))

if __name__ == "__main__":
    main()
 

