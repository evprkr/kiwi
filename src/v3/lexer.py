from parser import *
from token import *
from error import *

# CONSTANTS
NUMBERS = '0123456789'
ALPHAS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHANUMERICS = NUMBERS + ALPHAS

# POSITION TRACKING
class Position:
    def __init__(self, index, line, col, fname, text):
        self.index = index
        self.line = line
        self.col = col
        self.fname = fname
        self.text = text

    def adv(self, char=None, eol=False):
        self.index += 1
        self.col += 1

        if eol == True:
            self.line += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.index, self.line, self.col, self.fname, self.text)

# LEXER CLASS
class Lexer:
    def __init__(self, fname, text):
        self.fname = fname
        self.text = text
        self.pos = Position(-1, 0, -1, fname, text)
        self.char = None
        self.adv()

    def adv(self, eol=False):
        self.pos.adv(self.char, eol=eol)
        self.char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.char != None:
            if self.char in ' ': self.adv()
            elif self.char in NUMBERS: tokens.append(self.make_number())
            elif self.char in ALPHAS: tokens.append(self.make_identifier())
            elif self.char == '"': tokens.append(self.make_string()); self.adv()
            elif self.char == '+': tokens.append(Token(T_PLUS, pos_start = self.pos)); self.adv()
            elif self.char == '-': tokens.append(Token(T_MINUS, pos_start = self.pos)); self.adv()
            elif self.char == '*': tokens.append(Token(T_STAR, pos_start = self.pos)); self.adv()
            elif self.char == '/': tokens.append(Token(T_SLASH, pos_start = self.pos)); self.adv()
            elif self.char == '^': tokens.append(Token(T_POW, pos_start = self.pos)); self.adv()
            elif self.char == '(': tokens.append(Token(T_LPAREN, pos_start = self.pos)); self.adv()
            elif self.char == ')': tokens.append(Token(T_RPAREN, pos_start = self.pos)); self.adv()
            elif self.char == '=': tokens.append(Token(T_EQUAL, pos_start = self.pos)); self.adv()
            elif self.char == ';': tokens.append(Token(T_EOL, pos_start = self.pos)); self.adv(eol=True)
            else: return [], IllegalCharError(self.pos.copy(), self.pos , "'" + self.char + "'")

        tokens.append(Token(T_EOF, pos_start = self.pos))
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

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        self.adv()

        while self.char != None and self.char != '"':
            string += self.char
            self.adv()

        return Token(T_STRING, string, pos_start, self.pos)

    def make_identifier(self):
        identifier = ''
        pos_start = self.pos.copy()

        while self.char != None and self.char in ALPHANUMERICS + '_':
            identifier += self.char
            self.adv()

        if identifier in KEYWORDS: token_type = T_KEYWORD
        else: token_type = T_IDENT

        return Token(token_type, identifier, pos_start, self.pos)

# RUN PROGRAM
def run(fname, text):
    lexer = Lexer(fname, text)
    tokens, error = lexer.tokenize()
    if error: return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    return ast
