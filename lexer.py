# IMPORTS
from tokens import *
from errors import *
from parser import *
from interpreter import *

import string

# CONSTANTS
ALPHAS = string.ascii_letters
NUMBERS = '0123456789'
ALPHANUMERIC = ALPHAS + NUMBERS

# POSITION
class Position:
    def __init__(self, index, ln, col, fname, text):
        self.index = index
        self.ln = ln
        self.col = col
        self.fname = fname
        self.text = text

    def adv(self, char=None):
        self.index += 1
        self.col += 1

        if char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.index, self.ln, self.col, self.fname, self.text)

# LEXER
class Lexer:
    def __init__(self, fname, text):
        self.text = text
        self.pos = Position(-1, 0, -1, fname, text)
        self.char = None
        self.adv()

    def adv(self):
        self.pos.adv(self.char)
        self.char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.char != None:
            if self.char in ' ': self.adv()
            elif self.char in NUMBERS: tokens.append(self.make_number())
            elif self.char in ALPHAS: tokens.append(self.make_identifier())
            elif self.char == '+': tokens.append(Token(T_PLUS, pos_start = self.pos)); self.adv()
            elif self.char == '-': tokens.append(Token(T_MINUS, pos_start = self.pos)); self.adv()
            elif self.char == '*': tokens.append(Token(T_STAR, pos_start = self.pos)); self.adv()
            elif self.char == '/': tokens.append(Token(T_SLASH, pos_start = self.pos)); self.adv()
            elif self.char == '^': tokens.append(Token(T_POW, pos_start = self.pos)); self.adv()
            elif self.char == '=': tokens.append(Token(T_EQUAL, pos_start = self.pos)); self.adv()
            elif self.char == '(': tokens.append(Token(T_LPAREN, pos_start = self.pos)); self.adv()
            elif self.char == ')': tokens.append(Token(T_RPAREN, pos_start = self.pos)); self.adv()
            elif self.char == '"': tokens.append(self.make_string()); self.adv()
            else: return [], IllegalCharError(self.pos.copy(), self.pos, "'" + self.char + "'")

        tokens.append(Token(T_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        number = ''
        decimals = 0
        pos_start = self.pos.copy()

        while self.char != None and self.char in NUMBERS + '.':
            if self.char == '.':
                if decimals == 1: break
                decimals += 1
                number += '.'
            else:
                number += self.char
            self.adv()

        if decimals == 0: return Token(T_INT, int(number), pos_start, self.pos)
        return Token(T_FLOAT, float(number), pos_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.char != None and self.char in ALPHANUMERIC + '_':
            id_str += self.char
            self.adv()

        t_type = T_KEYWORD if id_str in KEYWORDS else T_IDENTIFIER
        return Token(t_type, id_str, pos_start, self.pos)

# RUN PROGRAM
global_symbol_table = SymbolTable()
global_symbol_table.set('null', Number(0))

def run(fname, text):
    # Generate tokens from raw code
    lexer = Lexer(fname, text)
    tokens, error = lexer.tokenize()
    if error: return None, error

    # Generate AST from tokens
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Interpret program from AST
    interpreter = Interpreter()
    context = Context('<module>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
