# KEYWORDS
T_NONE = 'NONE'
T_TRUE = 'TRUE'
T_FALSE = 'FALSE'
T_IF = 'IF'
T_ELSE = 'ELSE'
T_ELIF = 'ELIF'
T_AND = 'AND'
T_OR = 'OR'
T_PASS = 'PASS'
T_CLASS = 'CLASS'
T_FUNC = 'FUNC'
T_FOR = 'FOR'
T_WHILE = 'WHILE'
T_BREAK = 'BREAK'
T_TRY = 'TRY'
T_EXCEPT = 'EXCEPT'
T_REQUIRE = 'REQUIRE'

# NUMBER TOKENS
T_INT = 'INT'
T_FLOAT = 'FLOAT'

# MATH OPERATORS
T_PLUS = 'PLUS'
T_MINUS = 'MINUS'
T_STAR = 'STAR'
T_SLASH = 'SLASH'
T_MODULO = 'MODULO'

# DELIMITERS
T_LPAREN = 'LPAREN'
T_RPAREN = 'RPAREN'

# RELATIONAL OPERATORS
T_EQUAL = 'EQUAL'
T_EQEQUAL = 'EQEQUAL'
T_NOTEQUAL = 'NOTEQUAL'
T_LESSTHAN = 'LESSTHAN'
T_GREATERTHAN = 'GREATERTHAN'
T_LESSEQUAL = 'LESSEQUAL'
T_GREATEREQUAL = 'GREATEREQUAL'

class Token:
	def __init__(self, type_, value):
		self.type = type_
		self.value = value

	def __repr__(self):
		if self.value: return f'{self.type}:{self.value}'
		return f'{self.type}'

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
		self.post += 1
		self.current_char = self.text[pos] if self.pos < len(self.text) else None

	def make_tokens(self):
		tokens = []

		while self.current_char != None:
			if self.current_char in ' \t': self.advance()
			elif self.current_char in NUMBERS:
				tokens.append(self.make_number())
			elif self.current_char == '+':
				tokens.append(Token(T_PLUS)); self.advance()
			elif self.current_char == '-':
				tokens.append(Token(T_MINUS)); self.advance()
			elif self.current_char == '*':
				tokens.append(Token(T_STAR)); self.advance()
			elif self.current_char == '/':
				tokens.append(Token(T_SLASH)); self.advance()
			elif self.current_char == '(':
				tokens.append(Token(T_LPAREN)); self.advance()
			elif self.current_char == ')':
				tokens.append(Token(T_RPAREN)); self.advance()
		
		
		return tokens

	def make_number(self):
		num_str = ''
		dec_count = 0

		while self.current_char != None and self.current_char in NUMBERS + '.':
			if self.current_char == '.':
				dec_count += 1
				num_str += '.'
