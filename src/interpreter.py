from lexer import *
from parser import *
from errors import *
from tokens import *

# RUNTIME RESULT
class RuntimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

# VALUES
class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    # MATHEMATICAL OPERATIONS
    def math_add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def math_subtract(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def math_multiply(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def math_divide(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    other.pos_start, other.pos_end,
                    "Cannot divide by zero", self.context)

            return Number(self.value / other.value).set_context(self.context), None

    def math_power(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)

# CONTEXT
class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

# SYMBOL TABLE
class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

# INTERPRETER
class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node, context):
        return RuntimeResult().success(
            Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_VarAccessNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context))

        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_token.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinaryOpNode(self, node, context):
        res = RuntimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_token.type == T_PLUS:
            result, error = left.math_add(right)
        elif node.op_token.type == T_MINUS:
            result, error = left.math_subtract(right)
        elif node.op_token.type == T_STAR:
            result, error = left.math_multiply(right)
        elif node.op_token.type == T_SLASH:
            result, error = left.math_divide(right)
        elif node.op_token.type == T_POW:
            result, error = left.math_power(right)
        elif node.op_token.type == T_MOD:
            result, error = left.math_modulo(right)

        if error: return res.failure(error)
        else: return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RuntimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_token.type == T_MINUS:
            number, error = number.math_multiply(Number(-1))

        if error: return res.failure(error)
        else: return res.success(number.set_pos(node.pos_start, node.pos_end))
