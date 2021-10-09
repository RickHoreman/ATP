import Lexer
import Parser
import Interpreter
import sys
from utilities import parseRuntimeArguments, stringEndsWithAnyOf
from KeywordCollections import fileExtensions

arguments = sys.argv
if not stringEndsWithAnyOf(arguments[1], fileExtensions):
    print("Unsupported file extension.")
    exit(2)
filename = arguments[1]
parameters, options = parseRuntimeArguments(arguments[2:], [])

if 'D' in options:
    print("\nRunning lexer.")
tokens = Lexer.lex(filename)
if 'T' in options:
    print(f"Lexer ran in {Lexer.lex.time} seconds.")
if 'L' in options:
    print("Lexer Output (tokens):")
    for token in tokens:
        print(token)

if 'D' in options:
    print("\nRunning parser.")
ASTs = Parser.parse(tokens)
if 'T' in options:
    print(f"Parser ran in {Parser.parse.time} seconds.")
if 'P' in options:
    print("\nParser Output (AST):")
    print(f"Constructed {len(ASTs)} ASTs:")
    for ast in ASTs:
        print(ast)

if 'I' in options:
    if 'D' in options:
        print("\nRunning code.")
    result = Interpreter.run(ASTs, parameters)
    if 'T' in options:
        print(f"Code ran in {Interpreter.run.time} seconds.")
    if 'R' in options:
        print("\nInterpreter Output (result):")
    print(result)

    if 'T' in options:
        print(f"Total Interpreter run time: {Lexer.lex.time + Parser.parse.time + Interpreter.run.time}")

# Todo:
# TODO: Make README
# TODO: Make explanation video
# TODO: Add proper error handling
