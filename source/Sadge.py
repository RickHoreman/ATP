import Lexer
import Parser
import Interpreter
import sys

arguments = sys.argv
# TODO: Add argument checks, I.E. must at least contain a filename, check filename correctness, etc.

tokens = Lexer.lex("input/test-subroutines.sadge")
# print("Lexer Output (tokens):")
# for token in tokens:
#     print(token)

ASTs = Parser.parse(tokens)
print("\nParser Output (AST):")
print(f"Constructed {len(ASTs)} ASTs.\n")
for ast in ASTs:
    print(ast)

print("\nInterpreter Output (result):")
print(Interpreter.run(ASTs, arguments[1:]))



# All Todo:
# TODO: Add comments, lots of comments
# TODO: Add Haskell Typing to everything that doesnt have it yet
# TODO: Make README
# TODO: Make explanation video
# TODO: Add a decorator somewhere
# TODO: Add proper error handling

# Parser Todo:
# TODO: Add check to function call to make sure function exists //Can also be runtime
# TODO: maybe the same thing for variables //Can also be runtime
# TODO: Add support for function calls in expressions

# Interpreter Todo:
# TODO: Fuckin everything