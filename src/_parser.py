import errors
from lexer import *

class NumberNode:
    def __init__(self, token) -> None:
        self.token = token
      
    def __repr__(self) -> str:
        return f'Node: {self.token}'
    
class BinaryOpNode:
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f'Node: {self.left} {self.op} {self.right}'
    
class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.idx = 1 
        self.advance()

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]
    
    def __repr__(self) -> str:
        return f'{self.tokens}'

    def create_expression(self):
        left = 

    def create_factor(self):
        token = self.token

        if token.type in {T_INT, T_FLOAT}:
            self.advance()
            return NumberNode(token)
    
    def create_term(self):

        
     

    
    