import position

class Error:
    def __init__(self, start_pos, end_pos, type, contents) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.type = type
        self.contents = contents

    def string(self):
        return f'{self.type}: {self.contents}'
    
class InvalidCharacterError(Error):
    def __init__(self, contents) -> None:
        super().__init__('Invalid Character', contents)

class SyntaxError(Error):
    def __init__(self, contents) -> None:
        self.type = 'Syntax Error: '
        self.contents = contents

    def error_check(self):
        '''Check the type of Syntax Error to return the corresponding message'''
        if self.error_contents:
            pass
        