import Lexer
import Parser

tokens = Lexer.lex("input/test.sadge")
print("Lexer Output (tokens):")
for token in tokens:
    print(token)

print("\nParser Output (AST):")
ASTs = Parser.parse(tokens)
print(f"Constructed {len(ASTs)} ASTs.\n")
for ast in ASTs:
    print(ast)