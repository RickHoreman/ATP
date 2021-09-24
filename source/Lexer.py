from typing import List
import Tokens
import KeywordCollections as KC
# import sys
# sys.setrecursionlimit(200000)

# readFile :: String -> String
def readFile(inputFilePath : str) -> str:
    with open(inputFilePath, "r", encoding="utf8") as inputFile:
        return inputFile.read() 

# lexNext :: String -> Int -> Int -> List[Token] -> String -> Int -> List[Token]
def lexInt(input : str, lineNr : int, charNr : int, tokens : List[Tokens.Token], number : str='', value : int=0) -> List[Tokens.Token]:
    if len(input) <= 0:
        if KC.integers[number[-1]] in range(1,10):
            tokens.append(Tokens.Integer_Constant(lineNr, charNr-len(number), value + KC.integers[number[-1]]))
        else:
            tokens.append(Tokens.Integer_Constant(lineNr, charNr-len(number), value))
        return tokens
    char, *rest = input
    print(char)
    print(rest)
    if char not in KC.integers:
        if KC.integers[number[-1]] in range(1,10):
            #print(KC.integers[number[-1]])
            tokens.append(Tokens.Integer_Constant(lineNr, charNr-len(number), value + KC.integers[number[-1]]))
            return lexNext(input, lineNr, charNr, tokens)
        else:
            #print(value)
            tokens.append(Tokens.Integer_Constant(lineNr, charNr-len(number), value))
            return lexNext(input, lineNr, charNr, tokens)
    else:
        n = KC.integers[char]
        if n in range(1,10):
            if len(number)<=0:
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value)
            elif KC.integers[number[-1]] in range(1,10):
                tokens.append(Tokens.Integer_Constant(lineNr, charNr-len(number), value + KC.integers[number[-1]]))
                return lexNext(input, lineNr, charNr, tokens)
            else:
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value)
        else:
            if len(number)<=0:
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value + n)
            elif KC.integers[number[-1]] in range(1,10):
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value + (n * KC.integers[number[-1]]))
            else:
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value + n)
    

# lexNext :: String -> Int -> Int -> List[Token] -> List[Token]
def lexNext(input : str, lineNr : int, charNr : int, tokens : List[Tokens.Token]) -> List[Tokens.Token]:
    if len(input) <= 0:
        return tokens
    char, *rest = input
    if char == '\n':
        return lexNext(rest, lineNr + 1, 1, tokens)
    elif char == '〇':
        tokens.append(Tokens.Integer_Constant(lineNr, charNr, 0))
        return lexNext(rest, lineNr, charNr + 1, tokens)
    elif char in KC.integers:
        #print(input)
        return lexInt(input, lineNr, charNr, tokens)
    return lexNext(rest, lineNr, charNr + 1, tokens)

# lex :: String -> List[Token]
def lex(inputFilePath : str) -> List[Tokens.Token]:
    input = readFile(inputFilePath)
    return lexNext(input, 1, 1, [])

for token in lex("input/test.sadge"):
    print(token)