class Error:
    '''This class is the base class for all errors. It recieves the information
    errors from its derived classes and returns a formatted string containing
    the data provided. '''
    def __init__(self, idx, type, contents = None) -> None:
        '''Stores initialisation values when new instances of the Error Class
        are created'''
        self.idx = idx
        self.type = type
        self.contents = contents

    def __repr__(self) -> str:
        '''Returns the error message using the built in represent method'''
        return (f'{self.type} {self.contents} at column {self.idx.col}, ' 
    f'line {self.idx.line}') if self.contents else (f'{self.type} at '
    f'column {self.idx.col}, line {self.idx.line}')
    
    
class DivisionByZeroError(Error):
    '''This classs is derived from the Error class. It generates an error when
    division by zero occurs, and formats it before passing into to its
    parent class.'''
    def __init__(self, idx) -> None:
        super().__init__(idx, 'Division By Zero')


class ReassigmentError(Error):
    def __init__(self, idx, name) -> None:
        super().__init__(idx, f"Cannot Reassign '{name}'")


class DeclerationError(Error):
    '''This class generates an error when a function or variable is called
    but has not been declared'''
    def __init__(self, idx, type) -> None:
        super().__init__(idx, f"'{type}' was not declared")


class SyntaxError(Error):
    '''This class is derived from the Error class, but is also itself the base
    class for all Syntax Error types. It recieves the data on a Syntax Error
    and formats this before creating a super of Error and passing the
    information provided'''
    def __init__(self, idx, type, contents) -> None:
        '''Creates a super of the parent Error class allowing us to return our 
        error message'''
        super().__init__(idx, 'Syntax Error: ' + type, contents)


class InvalidCharacterError(SyntaxError):
    '''This class generates an error when an invalid character is found'''
    def __init__(self, idx, char) -> None:
        '''Creates a super of the parent Syntax Error class allowing us to 
        return our error message'''
        super().__init__(idx, 'Invalid Character', "'" + char + "'")


class DecimalsInFloat(SyntaxError):
    '''This class generates errors when there are the incorrect number of
    decimal points in a floating point number'''
    def __init__(self, idx, dot_count) -> None:
        '''Creates a super of the parent Syntax Error class allowing us to 
        return our error message'''
        super().__init__(idx, ('Expected Single Decimal in Floating Point ' 
                               'Number, recieved'), dot_count)
        

class Expected(SyntaxError):
    '''This class generates an error when the parser expects the code to follow
    a structure, but it does not''' 
    def __init__(self, idx, expected, type) -> None:
        super().__init__(idx, f'Expected {expected} following', 
                         "'" + type + "'")