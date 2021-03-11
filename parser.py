from tokens import *
from lexer import *

# NODES
class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'

class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f'({self.op_token}, {self.node})'

# PARSE RESULT
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def pass(self, node):
        self.node = node
        return self

    def fail(self, error):
        self.error = error
        return self

# PARSER
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.t_index = -1
        self.adv()

    def adv(self, ):
        self.t_index += 1
        if self.t_index < len(self.tokens):
            self.token = self.tokens[self.t_index]
        return self.token
