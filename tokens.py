class Token:
    def __init__(self, type_, val=None):
        self.type = type_
        self.val = val

    def __repr__(self):
        if self.val: return f'{self.type}:{self.val}'
        else: return f'{self.type}'

# DATA TYPES
T_INT =         'INT'
T_FLOAT =       'FLOAT'
T_STRING =      'STRING'

# MATH OPERATORS
T_PLUS =        'PLUS'
T_MINUS =       'MINUS'
T_STAR =        'STAR'
T_SLASH =       'SLASH'
T_MODULO =      'MODULO'

# DELIMITERS
T_LPAREN =      'LPAREN'
T_RPAREN =      'RPAREN'

# RELATIONAL OPERATORS
T_EQUAL =       'EQUAL'
T_EQEQUAL =     'EQEQUAL'
T_NOTEQUAL =    'NOTEQUAL'
T_LESSTHAN =    'LESSTHAN'
T_GREATTHAN =   'GREATTHAN'
T_LESSEQUAL =   'LESSEQUAL'
T_GREATEQUAL =  'GREATEQUAL'
