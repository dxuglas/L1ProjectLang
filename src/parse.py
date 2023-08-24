import errors
import position
from lexer import *

class ErrorNode:
    def __init__(self, error) -> None:
        '''This is the intialise function for the Error Node, storing the passed
        arguments'''
        self.error = error
        self.visit_name = 'error_node'

class FunctionAssignNode:
    def __init__(self, name, contents) -> None:
        '''This is the intialise function for the Function Assign Node, storing 
        the passed arguments'''
        self.name = name
        self.contents = contents
        self.visit_name = 'function_assign_node'

    def __repr__(self) -> str:
        '''This is the represent function, which returns the contents of the
        node in a neatly formatted way'''
        return self.name

class VarAssignNode:
    def __init__(self, name, value) -> None:
        '''This is the intialise function for the Variable Assign Node, storing 
        the passed arguments'''
        self.name = name
        self.value = value
        self.visit_name = 'var_assign_node'
        
class AccessNode:
    def __init__(self, name) -> None:
        '''This is the intialise function for the Access Node, storing the 
        passed arguments'''
        self.name = name
        self.visit_name = 'access_node'

class IfNode:
    def __init__(self, case, content, else_contents = None) -> None:
        '''This is the intialise function for the If Node, storing the passed
        arguments'''
        self.case = case
        self.contents = content
        self.else_contents = else_contents
        self.visit_name = 'if_node'

class LoopNode:
    def __init__(self, loop_count, content) -> None:
        '''This is the intialise function for the Loop Node, storing the passed
        arguments'''
        self.loop_count = loop_count
        self.content = content
        self.visit_name = 'loop_node'

class WhileNode:
    def __init__(self, case, content) -> None:
        '''This is the intialise function for the While Node, storing the passed
        arguments'''
        self.case = case
        self.content = content
        self.visit_name = 'while_node'

class StringNode:
    def __init__(self, token) -> None:
        '''This is the intialise function for the String Node, storing the 
        passed arguments'''
        self.token = token
        self.visit_name = 'string_node'

class NumberNode:
    def __init__(self, token, idx) -> None:
        '''This is the intialise function for the Number Node, storing the 
        passed arguments'''
        self.token = token
        self.idx = idx
        self.visit_name = 'number_node'
      
    def __repr__(self) -> str:
        '''This is the represent function, which returns the contents of the
        node in a neatly formatted way'''
        return f'{self.token}'
    
class BinaryOpNode:
    def __init__(self, left, op, right) -> None:
        '''This is the intialise function for the Binary Operator Node, storing 
        the passed arguments'''
        self.left = left
        self.op = op
        self.right = right
        self.visit_name = 'binary_op_node'

    def __repr__(self) -> str:
        '''This is the represent function, which returns the contents of the
        node in a neatly formatted way'''
        return f'({self.left} {self.op} {self.right})'
    
class UnaryOpNode:
    def __init__(self, op, node) -> None:
        '''This is the intialise function for the Unary Operator Node, storing 
        the passed arguments'''
        self.op = op
        self.node = node
        self.visit_name = 'unary_op_node'

    def __repr__(self) -> str:
        '''This is the represent function, which returns the contents of the
        node in a neatly formatted way'''
        return f'{self.op}{self.node}'
    
class Parser:
    def __init__(self, tokens) -> None:
        '''This function is called upon the creation of an instance of the
        parser, storing arguments and creating an index'''
        self.tokens = tokens
        self.token = self.tokens[0]
        self.idx = position.Position(-1, 1, 1)
        self.advance()

    def advance(self):
        '''This function advances through the list of nodes in the lexer,
        checking to ensure their isn't an index error'''
        self.idx.advance(self.token)
        if self.idx.idx < len(self.tokens):
            self.token = self.tokens[self.idx.idx]
    
    def __repr__(self) -> str:
        '''This is the represent function, which returns the tokens stored'''
        return f'{self.tokens}'
    
    def parse(self):
        '''This function starts the parsing process, and then returns the final
        results'''
        result = self.create_statments()
        return result 

    def create_statments(self):
        '''This function creates statments, which can be simply defined as
        sections of the code. '''
        statments = []
        
        # While the parser has not reached the end of the file passed
        while self.token.type != T_EOF: 
            # Create an expression and store the result in statments
            statments.append(self.create_expression())
            if self.token.value == 'end':
                self.advance()
            # Advance until a new statment is reached, allowing multiple lines
            # between pieces of code
            while self.token.type == T_NL:
                self.advance()
        return statments

    def create_expression(self):
        '''This function creates expresions, the highest level of the
        proccessing tree'''

        if self.token.value == 'variable':
            self.advance()

            # If the token following a variable decleration is not a name
            if self.token.type != T_IDENTIFIER:
                # Make a clone of the index
                idx = self.idx.clone()
                # Advance until the end of the variable decleration
                while self.token.type not in (T_NL, T_EOF):
                    self.advance()
                return ErrorNode(errors.Expected(idx, 'Identifier', 'variable'))
            
            name = self.token
            self.advance()
            
            # If the token following the name is not an assignment operator
            if self.token.type != T_EQL:
                idx = self.idx.clone()
                while self.token.type not in (T_NL, T_EOF):
                    self.advance()
                return ErrorNode(errors.Expected(idx, 'Assignment Operator', 'Identifier'))
            
            self.advance()

            value = self.create_expression()
            
            # If the no value is assigned
            if value == None:
                idx = self.idx.clone()
                return ErrorNode(errors.Expected(idx, 'Value', 'Assignment Operator'))
            
            return VarAssignNode(name, value)

        if self.token.value == 'if':
            self.advance()
            case = []

            if self.token.type in (T_IDENTIFIER, T_INT, T_FLOAT):
                case.append(self.create_expression())
            else:
                idx = self.idx.clone()
                while self.token.value != 'end':
                    self.advance()
                return ErrorNode(errors.Expected(idx, 'Comparitable Value', 'if'))

            if self.token.type in (T_EQLS, T_GRT, T_LESS, T_NEQL):
                case.append(self.token)
            else:
                idx = self.idx.clone()
                while self.token.value != 'end':
                    self.advance()
                return ErrorNode(errors.Expected(idx, 'Comparison Operator', 'Comparitable Value'))
            self.advance()

            if self.token.type in (T_IDENTIFIER, T_INT, T_FLOAT):
                case.append(self.create_expression())
            else:
                idx = self.idx.clone()
                while self.token.value != 'end':
                    self.advance()
                return ErrorNode(errors.Expected(idx, 'Comparitable Value', 'Comparison Operator'))
            
            while self.token.type == T_NL:
                self.advance()

            contents = []
            while self.token.value not in ('otherwise', 'end'):
                contents.append(self.create_expression())
                if self.token.type == T_NL:
                    self.advance()
                    continue
                else:
                    break

            while self.token.value == 'otherwise':
                else_contents = []
                while self.token.type == T_NL:
                    self.advance()
                while True:
                    if self.token.value == 'end':
                        break
                    else_contents.append(self.create_expression())
                    if self.token.type == T_NL:
                        self.advance()
                        continue
                    else:
                        break
            return IfNode(case, contents)
        
        if self.token.value == 'loop':
            self.advance()

            loop_count = None

            if self.token.type in (T_IDENTIFIER, T_INT, T_FLOAT):
                loop_count = self.create_expression()
            else:
                idx = self.idx.clone()
                while self.token.value != 'end':
                    self.advance()
                return ErrorNode(errors.Expected(idx, 'Number', 'loop'))
            
            while self.token.type == T_NL:
                self.advance()

            contents = []

            while True:
                if self.token.value == 'end':
                    break
                contents.append(self.create_expression())
                if self.token.type == T_NL:
                    self.advance()
                    continue
                else:
                    break

            return LoopNode(loop_count, contents)
        
        if self.token.value == 'while':
            self.advance()

            case = []

            if self.token.type in (T_IDENTIFIER, T_INT, T_FLOAT):
                case.append(self.create_expression())
            else:
                idx = self.idx.clone()
                while self.token.value != 'end':
                    self.advance()
                return ErrorNode(errors.Expected(idx, 'Comparitable Value', 'while'))


            if self.token.type in (T_EQLS, T_LESS, T_GRT, T_NEQL):
                case.append(self.token)
            else:
                idx = self.idx.clone()
                while self.token.value != 'end':
                    self.advance()
                return ErrorNode(errors.Expected(idx, 'Comparison Operator', 'Comparitable Value'))

            self.advance()

            if self.token.type in (T_IDENTIFIER, T_INT, T_FLOAT):
                case.append(self.create_expression())
            else:
                idx = self.idx.clone()
                while self.token.value != 'end':
                    self.advance()
                return ErrorNode(errors.Expected(idx, 'Comparitable Value', 'Comparison Operator'))
            
            while self.token.type == T_NL:
                self.advance()

            contents = []
            
            while True:
                if self.token.value == 'end':
                    break
                contents.append(self.create_expression())
                if self.token.type == T_NL:
                    self.advance()
                    continue
                else:
                    break
            
            return WhileNode(case, contents)

        if self.token.value == 'function':
            self.advance()

            if self.token.type != T_IDENTIFIER:
                idx = self.idx.clone()
                while self.token.value != 'end':
                    self.advance()
                return ErrorNode(errors.Expected(idx, 'Identifier', 'function'))
            
            name = self.token.value
            self.advance()
            self.advance()

            contents = []
            
            while self.token.value != 'end':
                contents.append(self.create_expression())
                if self.token.type == T_NL:
                    self.advance()
                    continue
                else:
                    break

            return FunctionAssignNode(name, contents)

        root = self.create_term()

        while self.token.type in (T_PLUS, T_MINUS):
            op = self.token
            self.advance()
            right = self.create_term()
            root = BinaryOpNode(root, op, right)
        
        return root
    
    def create_term(self):
        root = self.create_factor()

        while self.token.type in (T_MUL, T_DIV, T_POW):
            op = self.token
            self.advance()
            right = self.create_factor()
            root = BinaryOpNode(root, op, right)
        
        return root
    
    def create_factor(self):
        '''This function creates factors, the lowest level of the proccesing
        tree'''
        token = self.token
        if token.type in (T_PLUS, T_MINUS):
            op = token
            self.advance()
            node = self.create_factor()
            return UnaryOpNode(op, node)
        elif token.type in (T_INT, T_FLOAT):
            self.advance()
            return NumberNode(token, self.idx.clone())
        elif token.type == T_STRING:
            self.advance()
            return StringNode(token)
        elif token.type == T_LPAREN:
            self.advance()
            expression = self.create_expression()
            if self.token.type == T_RPAREN:
                return expression
            else:
                return ErrorNode(errors.Expected(self.idx, ')', '('))
        elif token.type == T_IDENTIFIER:
            self.advance()
            return AccessNode(token)