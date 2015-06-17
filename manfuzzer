#!/usr/bin/python3

"""   Copyright 2015 Peter Chapman, GGrieco

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

The ManFuzzer: Given a binary path this file produces test cases to that binary
based on the flags found in -h,-H,--help and the man page. There is also the
option to execute those test cases."""

import argparse
import logging
import sys
import manparser
import random
import time
import subprocess
from values.textgen import TextValueGenerator
from values.filegen import FileValueGenerator
from values.datagen import Int32ValueGenerator

import legacymanfuzzer
import os
import signal


DEFAULT_TEST_CASES = 1000
DEFAULT_PARAMS_MEAN = 1
DEFAULT_PARAMS_STDDEV = 2
DEFAULT_VALUES_PROB = 0.05
DEFAULT_TEXT_PROB = 1
DEFAULT_TEXT_MEAN = 20
DEFAULT_TEXT_STDDEV = 100
DEFAULT_FILE_PROB = 1
DEFAULT_FILE_MEAN = 20
DEFAULT_FILE_STDDEV = 100
DEFAULT_INT32_PROB = 1
DEFAULT_PROGRAM_INPUT_PROB = 0.05
DEFAULT_STDIN_PROB = 0.05
DEFAULT_TIMEOUT = 3
DEFAULT_EXECTIME = 60 * 10 # in seconds


def main():
    # Parse arguments
    argparser = argparse.ArgumentParser(description='''Produces and executes
    command-line inputs to an executable for fuzzing based on the flags found by
    running -h, -H, --help, and the man page for software testing.''')
    argparser.add_argument('-d','--debug',help="Enables debugging output.",action="store_true")
    argparser.add_argument('-v','--verbose',help="Enables verbose output. Debugging output includes verbose output.",action="store_true")
    argparser.add_argument('-n','--testcases',help="The maximum number of test cases to generate. The default value is %d." % DEFAULT_TEST_CASES,type=int,default=DEFAULT_TEST_CASES)
    argparser.add_argument('-e','--execute',help="Execute the generated test cases.",action="store_true")
    argparser.add_argument('-t','--timeout',help='The timeout in seconds for running an fuzz input.',default=DEFAULT_TIMEOUT,type=float)
    argparser.add_argument('--exectime',help='The amount of time in seconds to spend on a single program.',default=DEFAULT_EXECTIME,type=float)
    argparser.add_argument('--paramsmean',help="The mean number of parameters to use in generated test cases. The default number is %d." % DEFAULT_PARAMS_MEAN, type=float, default=DEFAULT_PARAMS_MEAN)
    argparser.add_argument('--paramsstddev', help="The standard deviation in the number of parameters to use in generated test cases. The default number is %d." % DEFAULT_PARAMS_STDDEV, type=float, default=DEFAULT_PARAMS_STDDEV)
    argparser.add_argument('--valuesprob',help="The probability parameters will be given values. The default probability is %d." % DEFAULT_VALUES_PROB, type=float, default=DEFAULT_VALUES_PROB)
    argparser.add_argument('--textprob',help="The probability text values will be used. The default probability is uniform between the other value types.", type=float, default=DEFAULT_TEXT_PROB)           
    argparser.add_argument('--textmean',help="The mean length of generated text values. The default mean length is %d." % DEFAULT_TEXT_MEAN, type=float, default=DEFAULT_TEXT_MEAN)
    argparser.add_argument('--textstddev', help="The standard deviation in the length of generated text values. The default is %d." % DEFAULT_TEXT_STDDEV, type=float, default=DEFAULT_TEXT_STDDEV)
    argparser.add_argument('--fileprob',help="The probability file values will be used. The default probability is uniform between the other value types.", type=float, default=DEFAULT_FILE_PROB)           
    argparser.add_argument('--filemean',help="The mean length of generated text values. The default mean length is %d." % DEFAULT_FILE_MEAN, type=float, default=DEFAULT_FILE_MEAN)
    argparser.add_argument('--filestddev', help="The standard deviation in the length of generated file values in bytes. The default is %d." % DEFAULT_FILE_STDDEV, type=float, default=DEFAULT_FILE_STDDEV)
    argparser.add_argument('--int32prob',help="The probability 32-bit integer values will be used. The default probability is uniform between the other value types.", type=float, default=DEFAULT_INT32_PROB)
    argparser.add_argument('--programinputprob', help="The probability of giving the entire program an input. The default is %d." % DEFAULT_PROGRAM_INPUT_PROB, type=float, default=DEFAULT_PROGRAM_INPUT_PROB)
    argparser.add_argument('--stdinprob', help="The probability of feeding a file in through standard input. The default is %d." % DEFAULT_STDIN_PROB, type=float, default=DEFAULT_STDIN_PROB)
    argparser.add_argument('--legacy', help="Runs manfuzzer in the legacy mode that performs better magically for certain inputs.", action="store_true")
    argparser.add_argument('executable', help='The relative or absolute path to the executable to be fuzzed.')
    

    args = argparser.parse_args()
    debuglogging = args.debug
    verboselogging = args.verbose
    # Create Logger
    loglevel = logging.WARNING
    
    if debuglogging == True:
        loglevel = logging.DEBUG
    elif verboselogging == True:
        loglevel = logging.INFO    
    
    logging.basicConfig(level=loglevel)
    logging.StreamHandler(sys.stderr)

    logger = logging.getLogger('man-fuzzer')
    
    logger.info("Logger setup complete.")
    
    # Extract command-line arguments
    executable = args.executable
    
    testcases = args.testcases    
    timeout = args.timeout
    exectime = args.exectime
    execute = args.execute
    
    paramsmean = args.paramsmean
    paramsstddev = args.paramsstddev
    programinputprob = args.programinputprob
    stdinprob = args.stdinprob
    valuesprob = args.valuesprob
    
    
    logger.debug("%d test cases requested." % testcases)
    logger.debug("Test cases will be generated with a mean number of parameters %f and standard deviation %f." % (paramsmean,paramsstddev))
    logger.info("Executable path: %s" % str(executable))   
    argumentgenerator = manparser.mineflags(executable)
    logger.debug("The mined flags: %s" % str(argumentgenerator))
    
    textmean = args.textmean
    textstddev = args.textstddev
    textprob = args.textprob
    textgen = TextValueGenerator(textmean,textstddev)
    
    
    filemean = args.filemean
    filestddev = args.filestddev
    fileprob = args.fileprob
    filegen = FileValueGenerator(filemean,filestddev)
    
    int32prob = args.int32prob
    int32gen = Int32ValueGenerator()

    sumprobs = sum([textprob, fileprob, int32prob])
    valuegens = {(textprob/sumprobs, textgen), (fileprob/sumprobs, filegen), (int32prob/sumprobs, int32gen)}

    legacy = args.legacy
    generator = lambda : generate_testcases(executable, argumentgenerator, valuegens, testcases = testcases, paramsmean = paramsmean, paramsstddev = paramsstddev, valuesprob = valuesprob,programinputprob = programinputprob, stdinprob = stdinprob) 
    if legacy:
        generator = lambda : legacymanfuzzer.legacy(executable,testcases,paramsmean,paramsstddev)
                 
    # Generate and possibly execute test cases
    start_time = time.time()
    for test_case in generator():        
        print(executable + ' ' + test_case)
        if execute:
            if time.time() - start_time > exectime:
                logger.info("Time has expired for fuzzing %s" % executable)
                break
            command = executable + " " + test_case
            logger.info("Executing command '%s'" % (command))
            try:
                run_command_check(command,timeout)
            except subprocess.CalledProcessError as e:                
                returncode = e.returncode
                if os.WIFSIGNALED(returncode) and os.WTERMSIG(returncode) == signal.SIGSEGV:                    
                    logger.warning("Crash (crash) input: %s" % str(command))
                    try: 
                        run_command("cp `ls -t /tmp/tmp* | head -1` tempfiles/.",1) # Save crash input        
                    except Exception as e:
                        logger.error("Could not copy temp file")
            except subprocess.TimeoutExpired:
                logger.info("Command timeout: %s" % str(command))                       
            except Exception as e:
                logger.error("Command failed: %s" % str(command))
                logger.exception(e)    
                
    
    # Close
def run_command(command,timeout):    
    return subprocess.call(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True,timeout = timeout)

def run_command_check(command,timeout):    
    return subprocess.check_call(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True,timeout = timeout)
    


def generate_testcases(executable, argumentgenerator, valuegens, testcases = DEFAULT_TEST_CASES, paramsmean = DEFAULT_PARAMS_MEAN, paramsstddev = DEFAULT_PARAMS_STDDEV, valuesprob = DEFAULT_VALUES_PROB, programinputprob = DEFAULT_PROGRAM_INPUT_PROB, stdinprob = DEFAULT_STDIN_PROB):
    
    generatedtestcases = set()
    for _ in range(testcases):
        num_flags_used = int(random.gauss(paramsmean, paramsstddev))
        num_flags_used = max(0, min(num_flags_used, argumentgenerator.size()))
        test_case = set()
        for _ in range(num_flags_used):
            test_case.add(argumentgenerator.genarg(value=(None if random.random() >= valuesprob else pickgen(valuegens).generate())))
        test_case = ' '.join(test_case)
        
        if random.random() <= programinputprob:
            test_case += ' ' + pickgen(valuegens).generate()
        if random.random() <= stdinprob:
            test_case += ' < ' + pickgen(valuegens).generate()    
            
        if test_case not in generatedtestcases:            
            generatedtestcases.add(test_case)
            yield test_case
            
    
    

def pickgen(valuegens):
    randomness = random.random()
    probsum = 0
    for prob,gen in valuegens:
        probsum += prob
        if randomness <= probsum:
            return gen


if __name__ == "__main__":
    main()






