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



# TODO: make AST printing pretty (enough for debugging)
# TODO: Add check to function call to make sure function exists
# TODO: maybe the same thing for variables
