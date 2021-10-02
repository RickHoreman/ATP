import Lexer
import Parser

tokens = Lexer.lex("input/test-subroutines.sadge")
# print("Lexer Output (tokens):")
# for token in tokens:
#     print(token)

ASTs = Parser.parse(tokens)
print("\nParser Output (AST):")
print(f"Constructed {len(ASTs)} ASTs.\n")
for ast in ASTs:
    print(ast)