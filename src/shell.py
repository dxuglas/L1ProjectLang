import lexer
import _parser
import interpreter

if __name__ == '__main__':
    line = input('> ')
    lexer = lexer.Lexer(line)
    tokens = lexer.create_tokens()
    parser = _parser.Parser(tokens)
    nodes = parser.parse()
    interpreter = interpreter.Interpreter()
    result = interpreter.visit(nodes)
    print(int(result.value) if float(result.value).is_integer() 
          else result.value)
    