import regex as rx
import errors
import position
import string 

# Constants
DIGITS = '0123456789'
LETTERS = string.ascii_letters

# Define the constant variables for token types.
# Operator tokens.
T_MUL = 'T_MUL'
T_DIV = 'T_DIV'
T_PLUS = 'T_PLUS'
T_MINUS = 'T_MINUS'
T_LPAREN = 'T_LPAREN'
T_RPAREN = 'T_RPAREN'
T_POW = 'T_POW'
# Data Type tokens.
T_INT = 'T_INT'
T_FLOAT = 'T_FLOAT'
T_STRING = 'T_STRING'
# Identifier tokens.
T_KEYWORD = 'T_KEYWORD'
T_IDENTIFIER = 'T_INDENTIFIER'
# Equal token;
T_EQL = 'T_EQL'
# End Of File token.
T_EOF = 'T_EOF'

KEYWORDS = [
    'variable'
]

# Create class to generate tokens.
class Token:
    def __init__(self, type, value = None) -> None:
        '''Initialises an instance of the token class, storing the passed
        arguments internally'''
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        '''Sets the representation of the class when it is printed'''
        if self.value != None: return f'{self.type}: {self.value}'
        else: return self.type

# Create lexer class to generate tokens based on user input.
class Lexer:
    def __init__(self, data) -> None:
        '''Initialises the lexer, and sets it up ready to create tokens.'''
        self.data = data
        self.idx = position.Position(0, 1, 1)
        self.char = self.data[0]

    def advance(self):
        '''Advances too the next character in the data, checking to ensure that
        there isn't an index error.'''
        self.idx.advance(self.char)
        if self.idx.idx < len(self.data):
            self.char = self.data[self.idx.idx]
        else:
            self.char = None

    def create_tokens(self):
        '''Creates tokens based on the data provided, checking for their type
        and assigning them to a list based on this.'''

        created_tokens = []

        while self.char != None:
            if self.char in {'\n', '\t', '\r', ' '}:
                self.advance()
            elif rx.match(r"[.a-zA-Z]", self.char):
                created_tokens.append(self.identifier_token())
            elif self.char in '0123456789':
                num, error = self.number_token()
                if error:
                    return None, error
                created_tokens.append(num)
            elif self.char == '+':
                created_tokens.append(Token(T_PLUS))
                self.advance()
            elif self.char == '-':
                created_tokens.append(Token(T_MINUS))
                self.advance()
            elif self.char == '/':
                created_tokens.append(Token(T_DIV))
                self.advance()
            elif self.char == '*':
                created_tokens.append(Token(T_MUL))
                self.advance()
            elif self.char == '(':
                created_tokens.append(Token(T_LPAREN))
                self.advance()
            elif self.char == ')':
                created_tokens.append(Token(T_RPAREN))
                self.advance()
            elif self.char == '^':
                created_tokens.append(Token(T_POW))
                self.advance()
            elif self.char == '=':
                created_tokens.append(Token(T_EQL))
                self.advance()
            else:
                return None, errors.InvalidCharactError(self.idx, self.char)

        created_tokens.append(Token(T_EOF))
        return created_tokens, None

    def number_token(self):
        '''Checks whether the current number is an Int or a Float and returns 
        a Token.'''

        num_as_str = ''
        dot_count = 0
        start_idx = self.idx.clone()

        while self.char != None and rx.match(r"[.0-9]", self.char):
            if self.char == '.':
               dot_count += 1
            num_as_str += self.char
            self.advance()
        
        if dot_count == 1: return Token(T_FLOAT, float(num_as_str)), None
        elif dot_count == 0: return Token(T_INT, int(num_as_str)), None
        else: return None, errors.DecimalsInFloat(start_idx, dot_count)

    def identifier_token(self):
        idf_as_str = ''

        while self.char != None and rx.match(r"[.0-9a-zA-Z_]", self.char):
            idf_as_str += self.char
            self.advance()

        if idf_as_str in KEYWORDS:
            return Token(T_KEYWORD, idf_as_str)
        return Token(T_IDENTIFIER, idf_as_str)