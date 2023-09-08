from lexer import * 
import operator

ops = {
    'T_EQLS' : operator.eq,
    'T_NEQL' : operator.ne,
    'T_LESS' : operator.lt,
    'T_GRT'  : operator.gt
}


class List():
    def __init__(self, list) -> None:
        '''This functions stores the list as it is intialised'''
        self.list = list

    def __repr__(self) -> str:
        '''This represent function generates a string containing all of the
        contents of the list formatted correctly.
        '''
        return_list = ''
        # For every element in the list add it to the string on its own line
        for element in self.list:
            return_list += f'{element}\n'
        return_list = return_list[:-1]
        return return_list


class String():
    def __init__(self, value) -> None:
        '''This function stores the value of a string as it is intialised.'''
        self.value = value

    def __repr__(self) -> str:
        '''This represent function returns the value of a string.'''
        return f'{self.value}'


class Number():
    def __init__(self, value, idx) -> None:
        '''This function stores the value of a number as intialised.'''
        self.value = value
        self.idx = idx
    
    def added_to(self, other):
        '''This function returns a number plus another.'''
        return Number(self.value + other.value, self.idx)
    
    def subbed_by(self, other):
        '''This function returns a number minus another.'''
        return Number(self.value - other.value, self.idx)
    
    def multed_by(self, other):
        '''This function returns a number multiplied by another.'''
        return Number(self.value * other.value, self.idx)

    def dived_by(self, other):
        '''This function returns a number divided by another.'''
        if other.value == 0:
            return errors.DivisionByZeroError(other.idx)

        return Number(self.value / other.value, self.idx)
    
    def pow(self, other):
        '''This function returns a number to the power of another.'''
        return Number(self.value ** other.value, self.idx)
    
    def __repr__(self) -> str:
        '''This represent function returns the value of the number.'''
        return f'{self.value}'
    

class Context():
    def __init__(self, name) -> None:
        self.name = name
        self.table = None


class SymbolTable():
    def __init__(self) -> None:
        '''This function is called when an instance of the symbol table is
        created.
        '''
        self.symbols = {}
        self.parent = None

    def get_value(self, name):
        '''This function retrieves the value of a symbol from the table.'''
        value = self.symbols.get(name)
        return value
    
    def set_value(self, name, value):
        '''This function stores the value of a symbol in the table.'''
        self.symbols[name] = value

    def set_function(self, name, value, idx):
        '''This function stores the value of functions in the table.'''
        if name in self.symbols:
           return errors.ReassigmentError(idx, name)
        self.symbols[name] = List(value)


class Interpreter:
    def visit(self, nodes, context):
        '''This is the visit function used externally to pass in a list of
        nodes to the interpreter.
        '''
        values = []
        for node in nodes:
            value = self.internal_visit(node, context)
            if value != None: values.append(value)
        return values

    def internal_visit(self, node, context):
        '''This is the visit function used internally to visit nodes stored
        inside other nodes.
        '''
        # Get the visit name of the current node and visit it. 
        method_name = f'visit_{node.visit_name}'
        method = getattr(self, method_name)
        return method(node, context)
    
    def evaluate_case(self, node, context):
        '''This function takes a node as an input and evaluates whether its
        case is True or False and then returns the value.
        '''
        # Get the value of all three parts of the case.
        primary = self.internal_visit(node.case[0], context).value
        op = node.case[1]
        secondary = self.internal_visit(node.case[2], context).value

        # Try to check whether the case is true or false.
        try: return ops[f'{op}'](primary, secondary)
        except: return False

    def visit_error_node(self, node, context):
        '''This is the visit function for Error Nodes. It returns the error
        stored inside.
        '''
        return node.error

    def visit_var_assign_node(self, node, context):
        '''This is the visit function for Variable Assing Nodes. It stores the
        value of the variable as a value in the symbol table.
        '''
        name = node.name.value
        value = self.internal_visit(node.value, context)
        error = context.table.set_value(name, value)
        if error:
            return error

    def visit_function_assign_node(self, node, context):
        '''This is the visit function for Function Assign Nodes. It stores the
        contents of the function as a value in the symbol table.
        '''
        name = node.name
        idx = node.idx
        contents = []
        # For every content node, append it to the new contents list once it
        # has been visited
        for content in node.contents:
            contents.append(self.internal_visit(content, context))
        error = context.table.set_function(name, contents, idx)
        if error:
            return error

    def visit_access_node(self, node, context):
        '''This is the visit function for Access Nodes. This accesses the
        values stored in the Symbol Table, and returns the value.
        '''
        name = node.name.value
        value = context.table.get_value(name)
        if value == None:
            return errors.DeclerationError(node.idx, node.name.value)
        return value

    def visit_if_node(self, node, context):
        '''This is the visit function for If nodes which takes a node as input,
        evaluates the case, and then returns the correct contents of the node.
        '''
        contents = []
        # If the case of the if statment is true:
        if self.evaluate_case(node, context):
            for content in node.contents:
                contents.append(self.internal_visit(content, context))
        # Else if the if statment has else contents:
        elif node.else_contents:
            for content in node.else_contents:
                contents.append(self.internal_visit(content, context))
        return List(contents)

    def visit_loop_node(self, node, context):
        '''This is the visit function for Loop Nodes. It checks the amount of
        times it needs to loop, and stores the resulting contents values in 
        turn. 
        '''
        contents = []

        # Check the loop value and run the for loop that many times. 
        for i in range(self.internal_visit(node.loop_count, context).value):
            for content in node.content:
                c = self.internal_visit(content, context)
                if c != None:
                    contents.append(c)
        return List(contents)
    
    def visit_while_node(self, node, context):
        '''This is the visit function for While Nodes. It evaluates the case,
        continuing to store the results of the loop while the case is true.
        '''
        contents = []
        # While the case of the while node is true:
        while self.evaluate_case(node, context):
            # Run trough the contents of the node and append them to contents
            for content in node.content:
                c = self.internal_visit(content, context)
                if c != None:
                    contents.append(c)

        return List(contents)

    def visit_string_node(self, node, context):
        '''This is the visit function for String Nodes, and simply returns
        the value of the node as a string.
        '''
        return String(node.token.value)

    def visit_number_node(self, node, context):
        '''This is the visit function for Number Nodes, and simply
        returns the value of the node as a number.
        '''
        return Number(node.token.value, node.idx)

    def visit_binary_op_node(self, node, context):
        '''This is the visit function for Binary Operator Nodes, and is
        responsible for handling maths operations.
        '''
        left = self.internal_visit(node.left, context)
        right = self.internal_visit(node.right, context)

        # Return the math function based on operator type.
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
        ''' This is the visit function for Unary Operator Nodes, it checks if
        the number is negative.
        '''

        number = self.internal_visit(node.node, context)

        # If the operator is '-' return the number as a negative
        if node.op.type == T_MINUS:
            number = number.multed_by(Number(-1))

        return number