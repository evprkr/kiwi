import lexer
import os, sys

def exit_shell():
    sys.exit(0);

if str(sys.argv[1]) == '-c': os.system('clear')

print(r"""
   ,--.,--.
  (  . \   \
  //_   `   |
 /' |       |
'    \      ;
   __|`--\,/ 
    /\    |
         ~|~""")
print("\nKiwi Shell v0.0.1")

while True:
    text = input('~ ')

    if text == 'exit': exit_shell()
    if text == 'clear': clear_shell() # throws an illegal character error

    result, error = lexer.run('$FILE', text)

    if error: print(error.as_string())
    else: print(result)
