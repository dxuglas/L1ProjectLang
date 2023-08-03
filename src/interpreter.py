from lexer import *

class Number():
    def __init__(self, value) -> None:
        self.value = value
    
    def added_to(self, other):
        return Number(self.value + other.value)
    
    def subbed_by(self, other):
        return Number(self.value - other.value)
    
    def multed_by(self, other):
        return Number(self.value * other.value)

    def dived_by(self, other):
        if other.value == 0:
            pass # RETURN ERROR DIV BYZ ERORIR

        return Number(self.value / other.value)
    
    def pow(self, other):
        return Number(self.value ** other.value)

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{node.visit_name}'
        method = getattr(self, method_name)
        return method(node)

    def no_visit_defined(self, node):
        print('no method defined')

    def visit_number_node(self, node):
        return Number(node.token.value)

    def visit_binary_op_node(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == T_MUL:
            return left.multed_by(right)
        elif node.op.type == T_DIV:
            return left.dived_by(right)
        elif node.op.type == T_PLUS:
            return left.added_to(right)
        elif node.op.type == T_MINUS:
            return left.subbed_by(right)
        elif node.op.type == T_POW:
            return left.pow(right)
        
    def visit_unary_op_node(self, node):
        number = self.visit(node.node)

        if node.op.type == T_MINUS:
            number = number.multed_by(Number(-1))
