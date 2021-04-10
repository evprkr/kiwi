class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.adv()

        if pos_end: self.pos_end = pos_end

    def is_type(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        else: return f'{self.type}'

# KEYWORDS
KEYWORDS = [
    'let',              # MUTABLE VARIABLE
    'set',              # IMMUTABLE VARIABLE
    'for',              # FOR LOOP
    'while',            # WHILE LOOP
    'func',             # DECLARE FUNCTION
]

# DATATYPES
T_INT =     'INT'       # INTEGER
T_FLOAT =   'FLOAT'     # FLOATING POINT
T_STRING =  'STRING'    # STRING

# OPERATORS
T_PLUS =    'PLUS'      # PLUS/POSITIVE
T_MINUS =   'MINUS'     # MINUS/NEGATIVE
T_STAR =    'STAR'      # STAR/MULTIPLY
T_SLASH =   'SLASH'     # SLASH/DIVIDE
T_POW =     'POW'       # POWER (EXPONENT)
T_LPAREN =  'LPAREN'    # LEFT PARENTHESIS
T_RPAREN =  'RPAREN'    # RIGHT PARENTHESIS

# COMPARATORS
T_EQUAL =   'EQUAL'     # SINGLE EQUALS
T_EQEQ =    'EQEQ'      # DOUBLE EQUALS

# RESERVED
T_FUNC =    'FUNC'      # DECLARE FUNCTION
T_IDENT =   'IDENT'     # VARIABLE IDENTIFIER
T_KEYWORD = 'KEYWORD'   # VARIABLE KEYWORD

# OTHERS
T_COMMENT = 'COMMENT'   # COMMENT (NO WAY!)
T_EOL =     'EOL'       # END OF LINE
T_EOF =     'EOF'       # END OF FILE
