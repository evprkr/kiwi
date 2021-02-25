import lexer
import os, sys

def exit_shell():
	sys.exit(0);

def clear_shell():
	os.system('clear')
	print("\nKiwi Shell v0.0.1")

print("\nKiwi Shell v0.0.1")

while True:
	text = input('~ ')

	if text == 'exit': exit_shell()
	if text == 'clear': clear_shell() # throws an illegal character error

	result, error = lexer.run(text)

	if error: print(error.as_string())
	else: print(result)
