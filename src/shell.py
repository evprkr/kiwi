# Kiwi Programming Language Rev

import lexer
import parser
import compiler

from tokens import *
from errors import *

import os, sys

# INFO
version = '0.3.0'

# SHELL FUNCTIONS
def exit_shell():
    sys.exit(0)

# SHELL ENTER
if len(sys.argv) > 1 and str(sys.argv[1]) == '-c': os.system('clear')

print(r"""
       ,--.,--.
      (  . \   \
      //_   `   |
     /' |       |
    '    \      ;
       __|`--\,/
        /\    |
             -|-""")
print(f"\n[ Kiwi Shell Rev {version} ]")

while True:
    text = input('>>--> ')
    
    if text == 'exit': exit_shell()
    else: result, error = lexer.run('$FILE', text)

    if error: print(error.as_string())
    else: print(f"OUTPUT: {result}\n")
