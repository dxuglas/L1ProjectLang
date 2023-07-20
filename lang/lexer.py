import regex as rx

# Define the constant variables for token types.
# Operator tokens.
T_MUL = 'T_MUL'
T_DIV = 'T_DIV'
T_PLUS = 'T_PLUS'
T_MINUS = 'T_MINUS'
T_LPAREN = 'T_LPAREN'
T_RPAREN = 'T_RPAREN'
# Data Type tokens.
T_INT = 'T_INT'
T_FLOAT = 'T_FLOAT'
T_STRING = 'T_STRING'
# End Of File token.
T_EOF = 'T_EOF'

# Create class to generate tokens.
class Token:
    def __init__(self, t_type, t_value) -> None:
        self.t_type = t_type
        self.t_value = t_value

# Create lexer class to generate tokens based on user input.
class Lexer:
    def __init__(self, data) -> None:
        self.data = data

        self.idx = 0 
        self.current_char = self.data[0]

    def advance(self):
        '''Advances too the next character in the data, checking to ensure that
        there isn't an index error.'''
        self.idx += 1
        if self.idx < len(self.data):
            self.current_char = self.data[self.idx]
        else:
            self.current_char = None

    def create_tokens(self):
        '''Creates tokens based on the data provided, checking for their type
        and assigning them to a list based on this.'''

        created_tokens = []

        while self.current_char != None:
            if self.current_char in {'\n', '\t', '\r', ' '}:
                self.advance()
            elif rx.match("[a-zA-Z]", self.current_char):
                self.advance()
                pass # TEMP TILL MAKE STRING
            elif self.current_char in '0123456789':
                self.create_number()
                self.advance()
            elif self.current_char == '+':
                created_tokens.append(T_PLUS)
                self.advance()
            elif self.current_char == '-':
                created_tokens.append(T_MINUS)
                self.advance()
            elif self.current_char == '/':
                created_tokens.append(T_DIV)
                self.advance()
            elif self.current_char == '*':
                created_tokens.append(T_MUL)
                self.advance()
            elif self.current_char == '(':
                created_tokens.append(T_LPAREN)
                self.advance()
            elif self.current_char == ')':
                created_tokens.append(T_RPAREN)
                self.advance()
            else: 
                created_tokens.append(T_EOF)

        return created_tokens
    
    def create_number(self):
        '''Generates a number token, checking wether it is a float or and int'''
        num_as_str = ''
        contains_dot = False

        while self.current_char != None and self.current_char in '.0123456789':
            if self.current_char == '.':
                if contains_dot:
                    # THROW ERROR FOR TWO DOTS
                    break
                contains_dot = True
                num_as_str += self.current_char
            else:
                num_as_str += self.current_char
        
        if contains_dot:
            return Token(T_FLOAT, float(num_as_str))
        else: return Token(T_INT, int(num_as_str))