from tokens import *
from errors import *
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

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'

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

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
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

    def parse(self):
        res = self.expr()
        if not res.error and self.token.type != T_EOF:
            return res.failure(InvalidSyntaxError(
                self.token.pos_start, self.token.pos_end,
                "Expected mathematical operator"))
        return res

    # FACTOR
    def factor(self):
        res = ParseResult()
        token = self.token

        if token.type in (T_PLUS, T_MINUS):
            res.register(self.adv())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token, factor))

        elif token.type in (T_INT, T_FLOAT):
            res.register(self.adv())
            return res.success(NumberNode(token))

        elif token.type in (T_LPAREN):
            res.register(self.adv())
            expr = res.register(self.expr())
            if res.error: return res
            if self.token.type == T_RPAREN:
                res.register(self.adv())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.token.pos_start, self.token.pos_end,
                    "Expected ')'"))

        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected INT or FLOAT"))

    def term(self): return self.binary_op(self.factor, (T_STAR, T_SLASH))
    def expr(self): return self.binary_op(self.term, (T_PLUS, T_MINUS))

    def binary_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.token.type in ops:
            op_token = self.token
            res.register(self.adv())
            right = res.register(func())
            if res.error: return res
            else: left = BinaryOpNode(left, op_token, right)

        return res.success(left)
