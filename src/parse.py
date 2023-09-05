import errors
import position
from lexer import *


class ErrorNode:
    def __init__(self, error) -> None:
        '''This is the intialise function for the Error Node, storing the 
        passed arguments'''
        self.error = error
        self.visit_name = 'error_node'
 

class FunctionAssignNode:
    def __init__(self, name, contents, idx) -> None:
        '''This is the intialise function for the Function Assign Node, storing 
        the passed arguments'''
        self.name = name
        self.contents = contents
        self.idx = idx
        self.visit_name = 'function_assign_node'

    def __repr__(self) -> str:
        '''This is the represent function, which returns the contents of the
        node in a neatly formatted way'''
        return self.name


class VarAssignNode:
    def __init__(self, name, value, idx) -> None:
        '''This is the intialise function for the Variable Assign Node, storing 
        the passed arguments'''
        self.name = name
        self.value = value
        self.idx = idx
        self.visit_name = 'var_assign_node'


class AccessNode:
    def __init__(self, name, idx) -> None:
        '''This is the intialise function for the Access Node, storing the 
        passed arguments'''
        self.name = name
        self.idx = idx
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
        '''This is the intialise function for the While Node, storing the 
        passed arguments'''
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

    def check_expected(self, expected, end, name, preceding):
        if self.token.type not in expected:
                # Make a clone of the index
                idx = self.idx.clone()
                # Advance until the end of the the decleration
                while self.token.type not in end:
                    self.advance()
                return ErrorNode(errors.Expected(idx, name, preceding))

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

            error = self.check_expected((T_IDENTIFIER), (T_NL, T_EOF), 
                                        'Identifier', 'variable')
            if error: return error
            
            name = self.token
            self.advance()  
            
            error = self.check_expected((T_EQL), (T_NL, T_EOF), 
                                        'Assignment Operator', 'Identifier')
            if error: return error
            
            self.advance()
            value = self.create_expression()
            
            # If the no value is assigned
            if value == None:
                # Make a clone of the index
                idx = self.idx.clone()
                return ErrorNode(errors.Expected(idx, 'Value', 
                                                 'Assignment Operator'))
            
            # Make a clone of the index and return the node
            idx = self.idx.clone()
            return VarAssignNode(name, value, idx)

        if self.token.value == 'if':
            self.advance()
            case = []
            
            error = self.check_expected((T_IDENTIFIER, T_INT, T_FLOAT), 
                                        ('end'), 'Comparitable Value', 'if')
            if error: return error
            
            # Append the value to the case
            case.append(self.create_expression())


            error = self.check_expected((T_EQLS, T_GRT, T_LESS, T_NEQL), 
                                        ('end'), 'Comparison Operator', 
                                        'Comparitable Value')
            if error: return error
            
            # Append the operator to the case
            case.append(self.token)
            self.advance()

            error = self.check_expected((T_IDENTIFIER, T_INT, T_FLOAT), 
                                        ('end'), 'Comparitable Value', 
                                        'Comparison Operator')
            if error: return error
            
            # Append the value to the case
            case.append(self.create_expression())

            # Advance while the token is T_NL
            while self.token.type == T_NL:
                self.advance()

            contents = []
            # While the token does not end the if statment
            while self.token.value not in ('otherwise', 'end'):
                # Append the content as an expression
                contents.append(self.create_expression())
                # Check if a new line is created after the expression
                if self.token.type == T_NL:
                    self.advance()
                # Otherwise return an error for two statments
                else:
                    break # ADD ERROR FOR TOO MANY STATMENTS ON ONE LINE

            # While the token is equal to otherwise (Allowing future
            # implimentation of otherwise if statments)
            while self.token.value == 'otherwise':
                else_contents = []
                # Advance while the token is T_NL
                while self.token.type == T_NL:
                    self.advance()
                # While the otherwise isn't ended
                while self.token.value != 'end':
                    # Append the contents as an expression
                    else_contents.append(self.create_expression())
                    # Check if a new line is created after the expression
                    if self.token.type == T_NL:
                        self.advance()
                    # Otherwise return error for two statments
                    else:
                        break

            return IfNode(case, contents)
        
        if self.token.value == 'loop':
            self.advance()
            loop_count = None

            error = self.check_expected((T_IDENTIFIER, T_INT, T_FLOAT), 
                                        ('end'), 'Number', 'loop')
            if error: return error
            
            loop_count = self.create_expression()
            
            # Advance until the contents is reached
            while self.token.type == T_NL:
                self.advance()

            contents = []
            # While the loop isn't ended, store the line in contents
            while self.token.value != 'end':
                contents.append(self.create_expression())
                if self.token.type == T_NL:
                    self.advance()
                else:
                    break

            self.advance()

            return LoopNode(loop_count, contents)
        
        if self.token.value == 'while':
            self.advance()
            case = []

            error = self.check_expected((T_IDENTIFIER, T_INT, T_FLOAT), 
                                        ('end'), 'Comparitable Value', 'while')
            if error: return error
            
            # Append the value to the case
            case.append(self.create_expression())


            error = self.check_expected((T_EQLS, T_GRT, T_LESS, T_NEQL), 
                                        ('end'), 'Comparison Operator', 
                                        'Comparitable Value')
            if error: return error
            
            # Append the operator to the case
            case.append(self.token)
            self.advance()

            error = self.check_expected((T_IDENTIFIER, T_INT, T_FLOAT), 
                                        ('end'), 'Comparitable Value', 
                                        'Comparison Operator')
            if error: return error

            # Advance until the contents code is reached
            while self.token.type == T_NL:
                self.advance()

            contents = []
            # While the while loop isn't ended store the line in contents
            while self.token.value != 'end':
                contents.append(self.create_expression())
                if self.token.type == T_NL:
                    self.advance()
                else:
                    break
            
            return WhileNode(case, contents)

        if self.token.value == 'function':
            self.advance()
            
            error = self.check_expected((T_IDENTIFIER), ('end'), 
                                        'Identifier', 'function')
            if error: return error

            name = self.token.value
            self.advance()
            # Advanced until the contained code is reached
            while self.token.type == T_NL:
                self.advance()

            contents = []
            # Until the function is ended, add the current line to contents
            while self.token.value != 'end':
                contents.append(self.create_expression())
                if self.token.type == T_NL:
                    self.advance()
                else:
                    break

            idx = self.idx.clone()
            return FunctionAssignNode(name, contents, idx)

        # Store the root node for maths operations
        root = self.create_term()
        # Run through the maths operations tree to term
        while self.token.type in (T_PLUS, T_MINUS):
            op = self.token
            self.advance()
            right = self.create_term()
            root = BinaryOpNode(root, op, right)
        
        return root
    
    def create_term(self):
        # Store the root node
        root = self.create_factor()

        # Run through the maths operations tree to factor
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

        # If the token is + or -
        if token.type in (T_PLUS, T_MINUS):
            # Store the token as an operator
            op = token
            self.advance()
            # Create a number node of the following token
            node = self.create_factor()
            return UnaryOpNode(op, node)
        # If the token is a number
        elif token.type in (T_INT, T_FLOAT):
            self.advance()
            # Return a number node
            return NumberNode(token, self.idx.clone())
        # If the token is a string
        elif token.type == T_STRING:
            self.advance()
            # Return a string node
            return StringNode(token)
        # If the token is (
        elif token.type == T_LPAREN:
            self.advance()
            # Create the expression inside the brackets
            expression = self.create_expression()
            # If the next token is a )
            if self.token.type == T_RPAREN:
                return expression
            # Otherwise return an error
            else:
                return ErrorNode(errors.Expected(self.idx, ')', '('))
        # If the token is an identifier
        elif token.type == T_IDENTIFIER:
            self.advance()
            # Return an access node
            return AccessNode(token, self.idx.clone())