import errors
from lexer import *

class FunctionAssignNode:
    def __init__(self, name, contents) -> None:
        self.name = name
        self.contents = contents
        self.visit_name = 'function_assign_node'

    def __repr__(self) -> str:
        return self.name

class VarAssignNode:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value
        self.visit_name = 'var_assign_node'
        
class AccessNode:
    def __init__(self, name) -> None:
        self.name = name
        self.visit_name = 'access_node'

class NumberNode:
    def __init__(self, token) -> None:
        self.token = token
        self.visit_name = 'number_node'
      
    def __repr__(self) -> str:
        return f'{self.token}'
    
class BinaryOpNode:
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.op = op
        self.right = right
        self.visit_name = 'binary_op_node'

    def __repr__(self) -> str:
        return f'({self.left} {self.op} {self.right})'
    
class UnaryOpNode:
    def __init__(self, op, node) -> None:
        self.op = op
        self.node = node
        self.visit_name = 'unary_op_node'

    def __repr__(self) -> str:
        return f'{self.op}{self.node}'
    
class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.idx = -1 
        self.advance()

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]
    
    def __repr__(self) -> str:
        return f'{self.tokens}'
    
    def parse(self):
        result = self.create_statments()
        return result 

    def create_statments(self):
        statments = []
        while self.token.type != T_EOF: 
            statments.append(self.create_expression())
            if self.token.value == 'end':
                self.advance()
            while self.token.type == T_NL:
                self.advance()
        return statments

    def create_expression(self):
        
        if self.token.value == 'variable':
            self.advance()

            if self.token.type != T_IDENTIFIER:
                return None # NEED TO ADD ERROR
            
            name = self.token
            self.advance()
            
            if self.token.type != T_EQL:
                return None # NEED TO ADD ERROR
            
            self.advance()
            value = self.create_expression()
            
            return VarAssignNode(name, value)

        if self.token.value == 'function':
            self.advance()

            if self.token.type != T_IDENTIFIER:
                return None # need to add error
            
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
        token = self.token
        if token.type in (T_PLUS, T_MINUS):
            op = token
            self.advance()
            node = self.create_factor()
            return UnaryOpNode(op, node)
        elif token.type in (T_INT, T_FLOAT):
            self.advance()
            return NumberNode(token)
        elif token.type == T_LPAREN:
            self.advance()
            expression = self.create_expression()
            if self.token.type == T_RPAREN:
                return expression
            else:
                #ERROR NO END PAREN
                pass
        elif token.type == T_IDENTIFIER:
            self.advance()
            return AccessNode(token)