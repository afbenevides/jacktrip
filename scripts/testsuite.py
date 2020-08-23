#!/usr/bin/env python3

import subprocess
import sys
import re

# list of test commands and expected results.
# Each test should be a tuple with the following format:
# (test command, expected return code, expected stdout, expected stderr, additional options)
# test command should be an array of the command string and arguments
# any of the other arguments can be None, but at least one of return code, stdout, or stderr
# should be defined.
# additional options:
# regex (True or False) match stdout/err with regex

# test command, expected return code, expected stdout, expected stderr, timeout, additional options

tests = [    
    # version test
    (["jacktrip", "-v"], 
        0,    # return code
        r"^JackTrip VERSION: 1\.2.*", # stdout
        None, # stderr
        1,    # timeout
        { 'regex': True }), # options
]


assert sys.version_info >= (3, 5)


class TestException(Exception):
    """ Exception generated when a test fails, including expected / received output. 
    """
    
    def __init__(self, command, expected, received):
        self.command = command
        self.expected = expected
        self.received = received
    
    def __str__(self):
        return "* failed: {test}\n- expected: {exp}\n- received: {recv}".format(test=" ".join(self.command), exp=self.expected, recv=self.received)


def matches(expected, received, regex=False):
    """ Return True or False depending on whether expected printed output matches. 
    """
    if regex:
        return re.match(expected, received.decode("utf-8").strip()) != None
    else:
        return stdout.str() == proc.stdout.decode("utf-8").strip()


def run_test(command, returncode, stdout, stderr, timeout, options):
    """ Test the provided command against expected result.
    """
    
    proc = subprocess.run(command, timeout=timeout, capture_output=True)
    
    if returncode and proc.returncode != returncode:
        raise TestException(command, returncode, proc.returncode)
    
    if stdout and not matches(stdout, proc.stdout, options['regex']):
        raise TestException(command, stdout.str(), proc.stdout.strip())
    
    if stderr and not matches(stderr, proc.stderr, options['regex']):
        raise TestException(command, stderr.strip(), proc.stderr.strip())


# defines for terminal colors
class termcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


num = len(tests)
run = 0
failed = 0

for test in tests:
    try:
        print("running test {n} of {num}".format(n=run, num=num))
        run_test(*test)
    except TestException as e:
        failed +=1 
        print(termcolors.RED + str(e) + termcolors.END)
    except Exception as e:
        failed +=1 
        print(str(e))
    run += 1

if failed > 0:
    final_color = termcolors.RED+termcolors.BOLD
else:
    final_color = termcolors.GREEN+termcolors.BOLD

print((final_color+"{num} tests, {passed} passed / {failed} failed"+termcolors.END).format(num=num, passed=(num-failed), failed=failed))
