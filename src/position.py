class Position:
    def __init__(self, idx, line, col) -> None:
        self.idx = idx
        self.line = line
        self.col = col

    def advance(self, char):
        self.col += 1
        self.idx += 1

        if char == '\n':
            self.line += 1
            self.col = 0
        
    def clone(self):
        return Position(self.idx, self.line, self.col)

        