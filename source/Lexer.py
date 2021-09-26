from typing import List
import Tokens
import KeywordCollections as KC
# import sys
# sys.setrecursionlimit(200000)

# readFile :: String -> String
def readFile(inputFilePath : str) -> str:
    with open(inputFilePath, "r", encoding="utf8") as inputFile:
        return inputFile.read() 

# listStartsWith :: List[String] -> List[String] -> Bool
def listStartsWith(list1 : List[str], list2 : List[str]) -> bool:
    if len(list2) <= 0:
        return True
    elif len(list1) <= 0:
        return False
    char1, *rest1 = list1
    char2, *rest2 = list2
    if char1 != char2:
        return False
    else:
        return listStartsWith(rest1, rest2)

# lexNext :: List[Char] -> Int -> Int -> List[Token] -> String -> Int -> List[Token]
def lexInt(input : List[str], lineNr : int, charNr : int, tokens : List[Tokens.Token], number : str='', value : int=0) -> List[Tokens.Token]:
    if len(input) <= 0:
        if KC.integers[number[-1]] in range(1,10):
            tokens.append(Tokens.Integer(lineNr, charNr-len(number), value + KC.integers[number[-1]]))
        else:
            tokens.append(Tokens.Integer(lineNr, charNr-len(number), value))
        return tokens
    char, *rest = input
    # ADD \n HANDLING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if char not in KC.integers:
        if KC.integers[number[-1]] in range(1,10):
            #print(KC.integers[number[-1]])
            tokens.append(Tokens.Integer(lineNr, charNr-len(number), value + KC.integers[number[-1]]))
            return lexNext(input, lineNr, charNr, tokens)
        else:
            #print(value)
            tokens.append(Tokens.Integer(lineNr, charNr-len(number), value))
            return lexNext(input, lineNr, charNr, tokens)
    else:
        n = KC.integers[char]
        if n in range(1,10):
            if len(number)<=0:
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value)
            elif KC.integers[number[-1]] in range(1,10):
                print(f"[Lexer] Syntax Error: Number attached to other number without spacing at line {lineNr}, char {charNr}.")
                tokens.append(Tokens.Integer(lineNr, charNr-len(number), value + KC.integers[number[-1]]))
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

# lexNext :: List[Char] -> Int -> Int -> List[Token] -> String -> List[Token]
def lexIdentifier(input : List[str], lineNr : int, charNr : int, tokens : List[Tokens.Token], name : str='') -> List[Tokens.Token]:
    if len(input) <= 0:
        print(f"[Lexer] Unexpected end of file at line {lineNr}, char {charNr}.")
        return tokens
    char, *rest = input
    if char == '\n':
        return lexIdentifier(rest, lineNr + 1, 1, tokens, name)
    elif char == 'さ':
        char2, *rest2 = rest
        if char2 == 'ん':
            tokens.append(Tokens.Identifier(lineNr, charNr-len(name), name + "さん"))
            return lexNext(rest2, lineNr, charNr+2, tokens)
    return lexIdentifier(rest, lineNr, charNr + 1, tokens, name + char)        

# lexNext :: List[Char] -> Int -> Int -> List[Token] -> List[Token]
def lexNext(input : List[str], lineNr : int, charNr : int, tokens : List[Tokens.Token]) -> List[Tokens.Token]:
    if len(input) <= 0:
        return tokens
    char, *rest = input
    if char == '\n':
        return lexNext(rest, lineNr + 1, 1, tokens)
    elif char == ' ':
        pass
    elif char == '〇':
        tokens.append(Tokens.Integer(lineNr, charNr, 0))
    elif char in KC.integers:
        return lexInt(input, lineNr, charNr, tokens)
    elif char == 'は':
        tokens.append(Tokens.Assignment(lineNr, charNr))
    elif listStartsWith(input, "です"):
        tokens.append(Tokens.Assignment_End(lineNr, charNr))
        return lexNext(rest[1:], lineNr, charNr + 2, tokens)
    elif listStartsWith(input, "yesh"):
        tokens.append(Tokens.Boolean(lineNr, charNr, True))
        return lexNext(rest[3:], lineNr, charNr + 4, tokens)
    elif listStartsWith(input, "nyet"):
        tokens.append(Tokens.Boolean(lineNr, charNr, False))
        return lexNext(rest[3:], lineNr, charNr + 4, tokens)
    elif listStartsWith(input, "F "):
        tokens.append(Tokens.Function_Definition(lineNr, charNr))
        return lexNext(rest[1:], lineNr, charNr + 2, tokens)
    elif listStartsWith(input, "OwO"):
        tokens.append(Tokens.Code_Block_Start(lineNr, charNr))
        return lexNext(rest[2:], lineNr, charNr + 3, tokens)
    elif listStartsWith(input, "UwU"):
        tokens.append(Tokens.Code_Block_End(lineNr, charNr))
        return lexNext(rest[2:], lineNr, charNr + 3, tokens)
    else:
        print(input)
        return lexIdentifier(input, lineNr, charNr, tokens)
    return lexNext(rest, lineNr, charNr + 1, tokens)

# lex :: String -> List[Token]
def lex(inputFilePath : str) -> List[Tokens.Token]:
    input = readFile(inputFilePath)
    return lexNext(list(input), 1, 1, [])

for token in lex("input/test.sadge"):
    print(token)