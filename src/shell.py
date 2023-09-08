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
    # Creates an instance of the Parser, and then generates nodes with the
    # passed Tokens
    nodes = parse.Parser(tokens).parse()
    # Creates a Symbol Table
    table = interpreter.SymbolTable()
    # Creates a context to store the Symbol Table in
    context = interpreter.Context('main')
    # Stores the Symbol Table in the context
    context.table = table

    # Creates an instance of the Interpreter and then interprets the passed
    # nodes into terminal outputs
    results = interpreter.Interpreter().visit(nodes, context)

    return results

if __name__ == '__main__':
        # Runs the user code, and stores the results
        results = run()
        for result in results:
            print(result)            