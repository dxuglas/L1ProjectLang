import lexer
import parse
import interpreter

import sys

def run():
    '''In this function we feed data through the transpiler'''

    # Takes the second argument in the terminal and opens the file
    data = sys.argv[1]
    data = open(data)

    # Creates an instance of the lexer class, and then generates tokens.
    tokens, error = lexer.Lexer(data.read()).create_tokens() 
    # If an error is returned by the lexer, return the error.
    if error:
        return error
    nodes = parse.Parser(tokens).parse()
    if error:
        return error

    table = interpreter.SymbolTable()
    context = interpreter.Context('main')
    context.table = table
    results = interpreter.Interpreter().primary_visit(nodes, context)
    return results

if __name__ == '__main__':
        results = run()
        for result in results:
            if isinstance(result, list):
                for secondary in result:
                    print(secondary)
            else:
                print(result)