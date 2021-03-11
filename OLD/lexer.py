from tokens import *

# ERRORS
class Error:
    def __init__(self, pos_start, pos_end, error_code, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_code = error_code
        self.details = details

    def as_string(self):
        result = f'\n{self.error_code}: {self.details}'
        result += f' in file {self.pos_start.fname}, at line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

# POSITION
class Position:
    def __init__(self, index, ln, col, fname, text):
        self. index = index
        self.ln = ln
        self.col = col
        self.fname = fname
        self.text = text

    def advance(self, current_char):
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.index, self.ln, self.col, self.fname, self.text)

# CONTANTS
NUMBERS = '0123456789'

# LEXER
class Lexer:
    def __init__(self, fname, text):
        self.fname = fname
        self.text = text
        self.pos = Position(-1, 0, -1, fname, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t': self.advance()
            elif self.current_char in NUMBERS: tokens.append(self.make_number())
            elif self.current_char == '+': tokens.append(Token(T_PLUS)); self.advance()
            elif self.current_char == '-': tokens.append(Token(T_MINUS)); self.advance()
            elif self.current_char == '*': tokens.append(Token(T_STAR)); self.advance()
            elif self.current_char == '/': tokens.append(Token(T_SLASH)); self.advance()
            elif self.current_char == '(': tokens.append(Token(T_LPAREN)); self.advance()
            elif self.current_char == ')': tokens.append(Token(T_RPAREN)); self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        
        return tokens, None

    def make_number(self):
        num_str = ''
        dec_count = 0

        while self.current_char != None and self.current_char in NUMBERS + '.':
            if self.current_char == '.':
                if dec_count == 1: break
                dec_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dec_count == 0:
            return Token(T_INT, int(num_str))
        else:
            return Token(T_FLOAT, float(num_str))

# RUN LEXER
def run(fname, text):
    lexer = Lexer(fname, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
