from tokens import *
from parser import *

# CONSTANTS
NUMBERS = '0123456789'

# ERRORS
class Error:
    def __init__(self, pos_start, pos_end, error, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error = error
        self.details = details

    def as_string(self):
        error_msg = f"{self.error}: {self.details}"
        error_msg += f" in file {self.pos_start.fname}, at line {self.pos_start.ln + 1}\n"
        return error_msg

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

# POSITION
class Position:
    def __init__(self, index, ln, col, fname, text):
        self.index = index
        self.ln = ln
        self.col = col
        self.fname = fname
        self.text = text

    def advance(self, char):
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
        self.pos.advance(self.char)
        self.char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.char != None:
            if self.char in ' \t': self.adv()
            elif self.char in NUMBERS: tokens.append(self.make_number()); self.adv()
            elif self.char == '+': tokens.append(Token(T_PLUS)); self.adv()
            elif self.char == '-': tokens.append(Token(T_MINUS)); self.adv()
            elif self.char == '*': tokens.append(Token(T_STAR)); self.adv()
            elif self.char == '/': tokens.append(Token(T_SLASH)); self.adv()
            elif self.char == '(': tokens.append(Token(T_LPAREN)); self.adv()
            elif self.char == ')': tokens.append(Token(T_RPAREN)); self.adv()
            elif self.char == '"': tokens.append(self.make_string()); self.adv()
            else: return [], IllegalCharError(self.pos.copy(), self.pos, "'" + self.char + "'")

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
    lexer = Lexer(fname, text)
    tokens, error = lexer.tokenize()

    return tokens, error
