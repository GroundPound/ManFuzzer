import logging
import random
import subprocess
import re


MAGIC_REGEX = '[\\s]\\-?\\-[\\w\\-]+'
DEFAULT_TEST_CASES = 1000
AVERAGE_PARAMETERS = 1
STDDEV_PARAMETERS = 2


def legacy(executable,combinations,mean,stddev):
    # Mine the flags
    hFlags = mine_h_flags(executable)
    HFlags = mine_H_flags(executable)
    helpFlags = mine_Help_flags(executable)
    manFlags = mine_Man_flags(executable)


    flags = hFlags | HFlags | helpFlags | manFlags # union everything together


    genderated_test_cases = set() # a set of sets for each test case (to remove repeated trials)


    for _ in range(combinations):
        num_flags_used = int(random.gauss(mean,stddev))
        num_flags_used = max(0,min(num_flags_used,len(flags)))
        test_case = frozenset(random.sample(flags,num_flags_used)) # created a test case!
        if test_case not in genderated_test_cases:
            genderated_test_cases.add(test_case)
            yield ' '.join(test_case)
    
    


def extract_arguments(command):
    try:
        child = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
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
