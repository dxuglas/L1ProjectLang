class Error:
    def __init__(self, error_type, error_contents) -> None:
        pass

    def string(self):
        return f'{self.error_type}: {self.error_contents}'
    
class InvalidCharacterError(Error):
    def __init__(self, error_contents) -> None:
        super().__init__('Invalid Character', error_contents)

class SyntaxError(Error):
    def __init__(self, error_contents) -> None:
        self.error_type = 'Syntax Error: '
        self.error_contents = error_contents

    def error_check(self):
        '''Check the type of Syntax Error to return the corresponding message'''
        if self.error_contents:
            pass
        