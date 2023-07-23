class NumberNode:
    def __init__(self, token) -> None:
        self.token = token
      
    def __repr__(self) -> str:
        return f'Token: {self.token}'
    
class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens