from lexer import *

from tokens import *
from errors import *

# BASIC NODES
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

# OPERATION NODES
class BinaryOpNode:
    def __init__(self, op_token, right_node, left_node):
        self.op_token = op_token
        self.left_node = left_node
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
        self.pos_end = self.node.pos_end

# VARIABLE NODES
class VarAssignNode:
    def __init__(self, var_ident, var_value, var_keyword):
        self.var_ident = var_ident
        self.var_value = var_value
        self.var_keyword = var_keyword

        self.pos_start = self.var_ident.pos_start
        self.pos_end = self.var_ident.pos_end

class VarAccessNode:
    def __init__(self, var_ident):
        self.var_ident = var_ident

        self.pos_start = self.var_ident.pos_start
        self.pos_end = self.var_ident.pos_end

# PARSER RESULT
class Result:
    def __init__(self):
        self.error = None
        self.node = None
        self.adv_count = 0

    def reg_adv(self):
        self.adv_count += 1

    def register(self, result):
        self.adv_count += result.adv_count
        if result.error: self.error = result.error
        return result.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.adv_count == 0:
            self.error = error
        return self

# MAIN PARSER
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.adv()

    def adv(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.token = self.tokens[self.index]
        return self.token

    def parse(self):
        result = self.expression()
        if not result.error and self.token.type != T_EOF:
            return result.failure(InvalidSyntaxError(
                self.token.pos_start, self.token.pos_end,
                "Expected operator"))
        return result

    # EGG 
    def egg(self):
        result = Result()
        token = self.token

        # NUMBER
        if token.type in (T_INT, T_FLOAT):
            result.reg_adv(); self.adv();
            return result.success(NumberNode(token))

        # STRING
        elif token.type == T_STRING:
            result.reg_adv(); self.adv();
            return result.success(StringNode(token))

        # IDENTIFIER
        elif token.type == T_IDENT:
            result.reg_adv(); self.adv();
            return result.success(VarAccessNode(token))

        # PARENTHETICAL
        elif token.type == T_LPAREN:
            result.reg_adv(); self.adv();
            expr = result.register(self.expression())
            if result.error: return result

            if self.token.type == T_RPAREN:
                result.reg_adv(); self.adv();
                return result.success(expr)
            else:
                return result.failure(InvalidSyntaxError(
                    self.token.pos_start, self.token.pos_end,
                    "Expected ')'"))
        
        # NONE OF THE ABOVE
        return result.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected int, float, identifier, or operator"))

    # POWER (moved to FACTOR)
    # def power(self):
    #    return self.binary_op(self.egg, (T_POW, ), self.factor)

    # FACTOR
    def factor(self):
        result = Result()
        token = self.token
        
        if token.type in (T_PLUS, T_MINUS):
            result.reg_adv(); self.adv();
            factor = result.register(self.factor())
            if result.error: return result
            return result.success(UnaryOpNode(token, factor))
   
        # POWER
        return self.binary_op(self.egg, (T_POW, ), self.factor)

    # TERM
    def term(self):
        return self.binary_op(self.factor, (T_STAR, T_SLASH))

    # EXPRESSION
    def expression(self):
        result = Result()

        # VARIABLE ASSIGNMENT
        if self.token.is_type(T_KEYWORD, self.token.value):
            keyword = self.token.value
            result.reg_adv(); self.adv();

            if self.token.type != T_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.token.pos_start, self.token.pos_end,
                    "Expected identifier"))

            var_ident = self.token
            result.reg_adv(); self.adv();

            if self.token.type != T_EQUAL:
                return result.failure(InvalidSyntaxError(
                    self.token.pos_start, self.token.pos_end,
                    "Expected '='"))

            result.reg_adv(); self.adv();
            expr = result.register(self.expression())
            if result.error: return result

            return result.success(VarAssignNode(var_ident, expr, keyword))

        node = result.register(self.binary_op(self.term, (T_PLUS, T_MINUS)))

        # ANYTHING ELSE
        if result.error:
            return result.failure(InvalidSyntaxError(
                self.token.pos_start, self.token.pos_end,
                "Expected int, float, keyword, identifier, or operator"))

        return result.success(node)

    # BINARY OPERATION
    def binary_op(self, func_a, operators, func_b=None):
        if func_b == None: # Only used for factors, not totally sure why?
            func_b = func_a

        result = Result()
        left = result.register(func_a())
        if result.error: return result

        while self.token.type in operators:
            op_token = self.token
            result.reg_adv(); self.adv()
            right = result.register(func_b())
            if result.error: return result
            else: left = BinaryOpNode(op_token, left, right)

        return result.success(left)
