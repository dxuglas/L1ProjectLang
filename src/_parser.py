import errors
from lexer import *

class NumberNode:
    def __init__(self, token) -> None:
        self.token = token
        self.name = 'number_node'
      
    def __repr__(self) -> str:
        return f'{self.token}'
    
class BinaryOpNode:
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.op = op
        self.right = right
        self.name = 'binary_op_node'

    def __repr__(self) -> str:
        return f'({self.left} {self.op} {self.right})'
    
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
        result, error = self.create_expression()
        return result, error

    def create_expression(self):
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

        if token.type in (T_INT, T_FLOAT):
            self.advance()
            return NumberNode(token)
    

        
     

    
    