import lexer
import parse
import interpreter

import sys

def run():
    '''In this function we feed data through the transpiler'''

    data = sys.argv[1]
    data = open(data)

    # Creates an instance of the lexer class, and then generates tokens.
    tokens, error = lexer.Lexer(data.read()).create_tokens() 
    # If an error is found during the lexical analysis, return the error.
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
            if result == None:
                continue
            if isinstance(result, list):
                for r in result:
                     print(r.value)
                continue
            print(result.value)
    
    