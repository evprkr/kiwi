from lexer import *
from token import *

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
	def __init__(self, left_node, right_node, op_token):
		self.left_node = left_node
		self.right_node = right_node
		self.op_token = op_token

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

    def register(self, result)
        self.adv_count += result.adv_count
        if res.error: self.error = res.error
        return res.node

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

    def adv_all(self, result):
        self.adv()
        result.reg_adv()

	def parse(self):
		result = self.expr()

    # EXPRESSIONS
    def expr(self)
        result = Result()

        # VARIABLE ASSIGNMENT
        if self.token.is_type(T_KEYWORD, self.token.value):
            keyword = self.token.value
            adv_all(result)

            if self.token.type != T_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.token.pos_start, self.token.pos_end,
                    "Expected identifier"))

            var_ident = self.token
            adv_all(result)

            if self.token.type != T_EQUAL:
                return result.failure(InvalidSyntaxError(
                    self.token.pos_start, self.token.pos_end,
                    "Expected '='"))

            adv_all(result)
            expr = result.register(self.expr())
            if result.error: return result

            return result.success(VarAssignNode(var_ident, expr, keyword))

        node = result.register(self.binary_op(self.term, (T_PLUS, T_MINUS)))

        if result.error:
            return res.failure(InvalidSyntaxError(
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
            adv_all()
            right = result.register(func_b())
            if result.error: return result
            else: left = BinaryOpNode(left, op_token, right)

        return result.success(left)
