import lexer
import _parser
import interpreter

def run():
    line = input('> ')

    tokens, error = lexer.Lexer(line).create_tokens()
    if error:
        return error

    nodes = _parser.Parser(tokens).parse()
    result = interpreter.Interpreter().visit(nodes)
    
    return result.value

if __name__ == '__main__':
    result = run()
    print(result)
    