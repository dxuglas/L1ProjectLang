import lexer
import _parser

if __name__ == '__main__':
    line = input('> ')
    lexer = lexer.Lexer(line)
    tokens = lexer.create_tokens()
    parser = _parser.Parser(tokens)
    print(parser)
    