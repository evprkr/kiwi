class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.adv()

        if pos_end: self.pos_end = pos_end

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
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
T_POW =         'POW'

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

# OTHER
T_EOF =         'EOF'
