import lexer, parser
import os, sys

if len(sys.argv) > 1 and str(sys.argv[1]) == '-c': os.system('clear')

print(r"""
   ,--.,--.
  (  . \   \
  //_   `   |
 /' |       |
'    \      ;
   __|`--\,/
    /\    |
         ~|~""")
print("\nKiwi Shell v0.0.2")

while True:
    text = input('~ ')
    result, error = lexer.run('$FILE', text)

    if text == 'exit': sys.exit(0)

    if error: print(error.as_string())
    else: print(f"\n{result}")
