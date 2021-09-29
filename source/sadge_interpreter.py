import Lexer
import Parser

tokens = Lexer.lex("input/test_parser.sadge")
print("Lexer Output (tokens):")
for token in tokens:
    print(token)

print("\nParser Output (AST):")
ASTs = Parser.parse(tokens)
for AST in ASTs:
    print(AST)