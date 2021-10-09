import Lexer
import Parser
import Interpreter
import sys

arguments = sys.argv
# TODO: Add argument checks, I.E. must at least contain a filename, check filename correctness, etc.
filename = "input/test-subroutines.sadge"
print("Running lexer.")
tokens = Lexer.lex(filename)
print(f"Lexer ran in {Lexer.lex.time} seconds.")
# print("Lexer Output (tokens):")
# for token in tokens:
#     print(token)

print("Running parser.")
ASTs = Parser.parse(tokens)
print(f"Parser ran in {Parser.parse.time} seconds.")
# print("\nParser Output (AST):")
# print(f"Constructed {len(ASTs)} ASTs:")
# for ast in ASTs:
#     print(ast)

print("Running code.")
result = Interpreter.run(ASTs, arguments[1:])
print(f"Code ran in {Interpreter.run.time} seconds.")
print("\nInterpreter Output (result):")
print(result)

print(f"Total Interpreter run time: {Lexer.lex.time + Parser.parse.time + Interpreter.run.time}")

# Todo:
# TODO: Add Haskell Typing to everything that doesnt have it yet
# TODO: Make README
# TODO: Make explanation video
# TODO: Add proper error handling
