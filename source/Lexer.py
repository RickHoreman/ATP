from typing import List
import Tokens

# readFile :: String -> String
def readFile(inputFilePath : str) -> str:
    with open(inputFilePath, "r") as inputFile:
        return inputFile.read() 

# lexNext :: String -> Int -> Int -> List[Token] -> List[Token]
def lexNext(input : str, lineNr : int, charNr : int, tokens : List[Tokens.Token]) -> None:
    if len(input) <= 0:
        return tokens
    char = input[0]
    if char == "\n":
        return lexNext(input[1:], lineNr + 1, 1, tokens)
    elif char == "1" or char == "2" or char == "3":
        tokens.append(Tokens.Primitive_Type(lineNr, charNr))
    return lexNext(input[1:], lineNr, charNr + 1, tokens)

# lex :: String -> List[Token]
def lex(inputFilePath : str) -> List[Tokens.Token]:
    input = readFile(inputFilePath)
    return lexNext(input, 1, 1, [])

for token in lex("input/test.sadge"):
    print(token)