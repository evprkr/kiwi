from tokens import *
from errors import *
from lexer import *
from interpreter import *

# NODES
class NumberNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token}'

class StringNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token}'

class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

        self.pos_start = self.op_token.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_token}, {self.node})'

class VarAssignNode:
    def __init__(self, var_name_token, value_node, var_type):
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.var_type = var_type

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end

class VarAccessNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end

# PARSE RESULT
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.adv_count = 0

    def register_adv(self):
        self.adv_count += 1

    def register(self, res):
        self.adv_count += res.adv_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.adv_count == 0:
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

    # OPERATIONS
    def atom(self):
        res = ParseResult()
        token = self.token

        if token.type in (T_INT, T_FLOAT):
            res.register_adv(); self.adv()
            return res.success(NumberNode(token))

        if token.type == T_STRING:
            res.register_adv(); self.adv()
            return res.success(StringNode(token))

        if token.type == T_IDENTIFIER:
            res.register_adv(); self.adv()
            return res.success(VarAccessNode(token))

        elif token.type == T_LPAREN:
            res.register_adv(); self.adv()
            expr = res.register(self.expr())
            if res.error: return res
            if self.token.type == T_RPAREN:
                res.register_adv(); self.adv()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.token.pos_start, self.token.pos_end,
                    "Expected ')'"))

        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected int, float, identifier, or operator"))

    def power(self):
        return self.binary_op(self.atom, (T_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        token = self.token

        if token.type in (T_PLUS, T_MINUS):
            res.register_adv(); self.adv()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token, factor))

        return self.power()

    def term(self):
        return self.binary_op(self.factor, (T_STAR, T_SLASH))

    def expr(self):
        res = ParseResult()

        if self.token.matches(T_KEYWORD, self.token.value):
            keyword = self.token.value
            res.register_adv(); self.adv()

            if self.token.type != T_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.token.pos_start, self.token.pos_end,
                    "Expected identifier"))

            var_name = self.token
            res.register_adv(); self.adv()

            if self.token.type != T_EQUAL:
                return res.failure(InvalidSyntaxError(
                    self.token.pos_start, self.token.pos_end,
                    "Expected '='"))

            res.register_adv(); self.adv()
            expr = res.register(self.expr())
            if res.error: return res

            return res.success(VarAssignNode(var_name, expr, keyword))

        node = res.register(self.binary_op(self.term, (T_PLUS, T_MINUS)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.token.pos_start, self.token.pos_end,
                "Expected int, float, var, identifier, or operator"))

        return res.success(node)

    def binary_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.token.type in ops:
            op_token = self.token
            res.register_adv(); self.adv()
            right = res.register(func_b())
            if res.error: return res
            else: left = BinaryOpNode(left, op_token, right)

        return res.success(left)
