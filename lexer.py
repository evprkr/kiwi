from tokens import *
from errors import *
from parser import *

# CONSTANTS
NUMBERS = '0123456789'

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
            elif self.char in NUMBERS: tokens.append(self.make_number());
            elif self.char == '+': tokens.append(Token(T_PLUS)); self.adv()
            elif self.char == '-': tokens.append(Token(T_MINUS)); self.adv()
            elif self.char == '*': tokens.append(Token(T_STAR)); self.adv()
            elif self.char == '/': tokens.append(Token(T_SLASH)); self.adv()
            elif self.char == '(': tokens.append(Token(T_LPAREN)); self.adv()
            elif self.char == ')': tokens.append(Token(T_RPAREN)); self.adv()
            elif self.char == '"': tokens.append(self.make_string()); self.adv()
            else: return [], IllegalCharError(self.pos.copy(), self.pos, "'" + self.char + "'") 

        tokens.append(Token(T_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        number = ''
        decimals = 0

        while self.char != None and self.char in NUMBERS + '.':
            if self.char == '.':
                if decimals == 1: break
                decimals += 1
                number += '.'
            else:
                number += self.char
            self.adv()

        if decimals == 0: return Token(T_INT, int(number))
        else: return Token(T_FLOAT, float(number))

    def make_string(self):
        string = '"'
        self.adv()

        while self.char != None and self.char != '"':
            string += self.char
            self.adv()

        string += '"'
        return Token(T_STRING, string)

# RUN LEXER
def run(fname, text):
    # Generate tokens from raw code
    lexer = Lexer(fname, text)
    tokens, error = lexer.tokenize()

    # Generate AST from tokens
    parser = Parser(tokens)
    ast = parser.parse()

    return tokens, error
