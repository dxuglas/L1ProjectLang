import errors
from lexer import *

class VarAssignNode:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value
        self.visit_name = 'var_assign_node'
        
class VarAccessNode:
    def __init__(self, name) -> None:
        self.name = name
        self.visit_name = 'var_access_node'

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
        result = self.create_expression()
        return result 

    def create_expression(self):
        if self.token.value == 'VAR':
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
            return VarAccessNode(token)