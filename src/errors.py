import position

class Error:
    def __init__(self, start_idx, end_idx, type, contents) -> None:
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.type = type
        self.contents = contents

    def string(self):
        return f'{self.type}: {self.contents}'
    
class InvalidCharacterError(Error):
    def __init__(self, start_idx, end_idx, contents) -> None:
        super().__init__(start_idx, end_idx, 'Invalid Character', contents)

class SyntaxError():
    def __init__(self, type, contents, pos) -> None:
        self.type = type
        self.contents 
        self.pos = pos
        

        