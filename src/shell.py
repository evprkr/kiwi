import lexer
import parser
import interpreter
import tokens
import errors

import os, sys

# INFO
version = '0.0.7'

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
print(f"\nKiwi Shell v{version}")

while True:
    text = input('~ ')
    
    if text == 'exit': exit_shell()
    else: result, error = lexer.run('$FILE', text)

    if error: print(error.as_string())
    else: print(f"{result}\n")
