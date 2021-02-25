import lexer
import sys

print("\nKiwi Shell v0.0.1")

while True:
    text = input('~ ')
    if text == 'exit': sys.exit(0)
    result, error = lexer.run(text)

    if error: print(error.as_string())
    else: print(result)
