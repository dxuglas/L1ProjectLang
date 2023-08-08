import lexer
import parse
import interpreter

def run():
    '''In this function we feed data through the transpiler'''
    line = input('> ')

    # Creates an instance of the lexer class, and then generates tokens.
    tokens, error = lexer.Lexer(line).create_tokens() 
    # If an error is found during the lexical analysis, return the error.
    if error:
        return error

    nodes = parse.Parser(tokens).parse()
    if error:
        return error
    
    table = interpreter.SymbolTable()
    context = interpreter.Context('main')
    context.table = table
    result = interpreter.Interpreter().visit(nodes, context)
    
    return result.value

if __name__ == '__main__':
    while True:
        result = run()
        print(result)
    
    