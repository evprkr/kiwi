import lexer, parser, interpreter, tokens, errors
import os, sys

# INFO
version = '0.0.3'

# SHELL FUNCTIONS
def run_program():
    pass

def exit_shell():
    sys.exit(0)

def about_kiwi():
    print(f"\nKiwi v{version} by Evan Parker (evprkr)")
    print("https://github.com/evprkr/kiwi\n")

def help_text():
    print("Perform basic operations right from the shell, or execute Kiwi scripts (.kw files) by passing the file name (with extension) to the shell.", end=' ')
    print("You can run Kiwi scripts from outside the Kiwi shell with the command 'kiwi MyScript.kw'\n")

shell_commands = [
    ['kiwi', run_program],
    ['exit', exit_shell],
    ['about', about_kiwi],
    ['help', help_text]
]

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

    for i in range(len(shell_commands)):
        if text in shell_commands[i][0]:
            func = shell_commands[i][1]
            func()
            break
    else:
        result, error = lexer.run('$FILE', text)

        if error: print(error.as_string())
        else: print(f"{result}\n")
