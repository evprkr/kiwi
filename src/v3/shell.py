import lexer, parser

from token import *
from error import *


import os, sys

os.system('clear')
print('Pixie Shell')

while True:
	text = input('&* ')

	if text == 'exit': sys.exit(0)
	else: result = lexer.run('$FILE', text)
	#else: result, error = lexer.run('$FILE', text)

	#if error: print(error.as_string())
	#else: print(f"{result}\n")
	print(f"{result}\n")
