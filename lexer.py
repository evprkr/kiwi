from tokens import *

# ERRORS
class Error:
    def __init__(self, error_code, details):
        self.error_code = error_code
        self.details = details

    def as_string(self):
        result = f'\n{self.error_code}: {self.details}'
        return result

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

# CONTANTS
NUMBERS = '0123456789'

# LEXER
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

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
            else: char = self.current_char; self.advance(); return [], IllegalCharError("'"+char+"'")
        
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
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()

    return tokens, error
