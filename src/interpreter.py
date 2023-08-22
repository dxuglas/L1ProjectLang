from lexer import *
import operator

ops = {
    'T_EQLS' : operator.eq,
    'T_NEQL' : operator.ne,
    'T_LESS' : operator.lt,
    'T_GRT'  : operator.gt
}

class String():
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

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
    
    def __repr__(self) -> str:
        return f'{self.value}'
    
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
            value = self.secondary_visit(node, context)
            if value != None: values.append(value)
        return values

    def secondary_visit(self, node, context):
            method_name = f'visit_{node.visit_name}'
            method = getattr(self, method_name)
            return method(node, context)
    


    def evaluate_case(self, node, context):
        '''This function takes a node as an input and evaluates whether its
        case is True or False and then returns the value'''
        primary = self.secondary_visit(node.case[0], context).value
        op = node.case[1]
        secondary = self.secondary_visit(node.case[2], context).value

        return ops[f'{op}'](primary, secondary)

    def visit_error_node(self, node, context):
        return node.error

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
        '''This is the visit function for If nodes which takes a node as input,
        evaluates the case, and then returns the correct contents of the node.'''
        contents = []
        if self.evaluate_case(node, context):
            for content in node.contents:
                contents.append(self.secondary_visit(content, context))
        elif node.else_contents:
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
        while True:
            if self.evaluate_case(node, context):
                for content in node.content:
                    contents.append(self.secondary_visit(content, context))
            else:
                break

        return contents

    def visit_string_node(self, node, context):
        return String(node.token.value)

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