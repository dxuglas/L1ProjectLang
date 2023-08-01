import lexer
import _parser
import interpreter

def run():
    '''In this function we feed data through the transpiler'''
    line = input('> ')

    # Creates an instance of the lexer class, and then generates tokens.
    tokens, error = lexer.Lexer(line).create_tokens() 
    # If an error is found during the lexical analysis, return the error.
    if error:
        return error

    nodes, error = _parser.Parser(tokens).parse()
    if error:
        return error
    result = interpreter.Interpreter().visit(nodes)
    
    return result.value

if __name__ == '__main__':
    result = run()
    print(result)
    
    