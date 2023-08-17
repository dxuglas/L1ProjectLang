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
    
class Context():
    def __init__(self, name) -> None:
        self.name = name
        self.table = None

class SymbolTable():
    def __init__(self) -> None:
        self.symbols = {}
        self.parent = None

    def get_value(self, name):
        value = self.symbols.get(name)
        return value
    
    def set_value(self, name, value):
        self.symbols[name] = value

class Interpreter:
    def primary_visit(self, nodes, context):
        values = []
        for node in nodes:
            values.append(self.secondary_visit(node, context))
        return values

    def secondary_visit(self, node, context):
            method_name = f'visit_{node.visit_name}'
            method = getattr(self, method_name)
            return method(node, context)

    def no_visit_defined(self, node):
        print('no method defined')

    def visit_var_assign_node(self, node, context):
        name = node.name.value
        value = self.secondary_visit(node.value, context)
        context.table.set_value(name, value)

    def visit_function_assign_node(self, node, context):
        name = node.name
        contents = []
        for content in node.contents:
            contents.append(self.secondary_visit(content, context))
        context.table.set_value(name, contents)

    def visit_access_node(self, node, context):
        name = node.name.value
        value = context.table.get_value(name)
        return value

    def visit_if_node(self, node, context):
        case = node.case
        contents = []
        if case[1].type == T_EQLS:
            if self.secondary_visit(case[0], context).value == self.secondary_visit(case[2], context).value:
                for content in node.contents:
                    contents.append(self.secondary_visit(content, context))
            else:
                for content in node.else_contents:
                    contents.append(self.secondary_visit(content, context))
        return contents

    def visit_loop_node(self, node, context):
        contents = []
        for i in range(self.secondary_visit(node.loop_count, context).value):
            for content in node.content:
                contents.append(self.secondary_visit(content, context))

        return contents
    
    def visit_while_node(self, node, context):
        contents = []
        case = node.case
        if case[1].type == T_LESS:
            while True:
                if self.secondary_visit(case[0], context).value < self.secondary_visit(case[2], context).value:
                    for content in node.content:
                        contents.append(self.secondary_visit(content, context))
                else:
                    break
        return contents

    def visit_number_node(self, node, context):
        return Number(node.token.value)

    def visit_binary_op_node(self, node, context):
        left = self.secondary_visit(node.left, context)
        right = self.secondary_visit(node.right, context)

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
        
    def visit_unary_op_node(self, node, context):
        number = self.secondary_visit(node.node, context)

        if node.op.type == T_MINUS:
            number = number.multed_by(Number(-1))

        return number