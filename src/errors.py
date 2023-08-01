import position

class Error:
    '''This class is the base class for all errors. It recieves the information
    errors from its derived classes and returns a formatted string containing
    the data provided. '''
    def __init__(self, idx, type, contents) -> None:
        self.idx = idx
        self.type = type
        self.contents = contents

    def __repr__(self) -> str:
        return (f'{self.type} {self.contents} at column {self.idx.col}, ' 
                f'line {self.idx.line}')

class SyntaxError(Error):
    '''This class is derived from the Error class, but is also itself the base
    class for all Syntax Error types. It recieves the data on a Syntax Error
    and formats this before creating a super of Error and passing the
    information provided'''
    def __init__(self, idx, type, contents) -> None:
        super().__init__(idx, 'Syntax Error: ' + type, contents)

class InvalidCharacterError(SyntaxError):
    def __init__(self, idx, char) -> None:
        super().__init__(idx, 'Invalid Character', "'" + char + "'")

class DecimalsInFloat(SyntaxError):
    def __init__(self, idx, dot_count) -> None:
        super().__init__(idx, (f'Expected Single Decimal in Floating Point ' 
                               'Number, recieved'), dot_count)