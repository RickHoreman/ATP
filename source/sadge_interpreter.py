import Lexer
import Parser

tokens = Lexer.lex("input/test-subroutines.sadge")
print("Lexer Output (tokens):")
for token in tokens:
    print(token)

print("\nParser Output (AST):")
ASTs = Parser.parse(tokens)
for ast in ASTs:
    print(ast)

print(len(None))