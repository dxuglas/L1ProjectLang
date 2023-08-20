import lexer

class Position:
    def __init__(self, idx, line, col) -> None:
        self.idx = idx
        self.line = line
        self.col = col

    def advance(self, current):
        self.col += 1
        self.idx += 1

        if isinstance(current, str):
            if current  == '\n':
                self.line += 1
                self.col = 0
        elif isinstance(current, lexer.Token):
            if current.type == lexer.T_NL:
                self.line += 1
                self.col = 0
        
    def clone(self):
        return Position(self.idx, self.line, self.col)