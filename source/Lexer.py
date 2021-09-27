from typing import Callable, List
import Tokens
import For_Loop_Tokens as FL_Tokens
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

# findMapped :: List[String] -> List[String] -> Bool -> List[String] -> List[String] -> Int -> Int
def findMapped(f : Callable[[List[str], List[str]], bool], list1 : List[str], list2 : List[str], depth : int=0) -> int:
    if len(list2) <= 0:
        return -1
    head, *tail = list2
    if f(list1, list(head)):
        return depth
    else:
        return findMapped(f, list1, tail, depth+1)

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
            tokens.append(Tokens.Integer(lineNr, charNr-len(number), value + KC.integers[number[-1]]))
            return lexNext(input, lineNr, charNr, tokens)
        else:
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
    else:
        index = findMapped(listStartsWith, input, KC.honorifics)
        if index >= 0:
            tokens.append(Tokens.Identifier(lineNr, charNr-len(name), name + KC.honorifics[index]))
            return lexNext(rest[len(KC.honorifics[index])-1:], lineNr, charNr+len(KC.honorifics[index]), tokens)
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
    elif char == '「':
        tokens.append(Tokens.Parameter_List_Open(lineNr, charNr))
    elif char == '」':
        tokens.append(Tokens.Parameter_List_Close(lineNr, charNr))
    elif char == '山':
        tokens.append(Tokens.Endline(lineNr, charNr))
    elif char == '+':
        tokens.append(Tokens.Addition(lineNr, charNr))
    elif char == '-':
        tokens.append(Tokens.Subtraction(lineNr, charNr))
    elif listStartsWith(input, ">="):
        tokens.append(Tokens.Greater_Than_Or_Equal(lineNr, charNr))
        return lexNext(rest[1:], lineNr, charNr + 2, tokens)
    elif listStartsWith(input, "<="):
        tokens.append(Tokens.Smaller_Than_Or_Equal(lineNr, charNr))
        return lexNext(rest[1:], lineNr, charNr + 2, tokens)
    elif char == '>':
        tokens.append(Tokens.Greater_Than(lineNr, charNr))
    elif char == '<':
        tokens.append(Tokens.Smaller_Than(lineNr, charNr))
    elif listStartsWith(input, "ですか？"):
        tokens.append(Tokens.If_Statement(lineNr, charNr))
        return lexNext(rest[3:], lineNr, charNr + 4, tokens)
    elif listStartsWith(input, "です"):
        tokens.append(Tokens.Assignment_End(lineNr, charNr))
        return lexNext(rest[1:], lineNr, charNr + 2, tokens)
    elif listStartsWith(input, "ね～"):
        tokens.append(Tokens.If_Statement_Continuation(lineNr, charNr))
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
        tokens.append(Tokens.Code_Block_Open(lineNr, charNr))
        return lexNext(rest[2:], lineNr, charNr + 3, tokens)
    elif listStartsWith(input, "UwU"):
        tokens.append(Tokens.Code_Block_Close(lineNr, charNr))
        return lexNext(rest[2:], lineNr, charNr + 3, tokens)
    elif listStartsWith(input, "yeet"):
        tokens.append(Tokens.Return_Statement(lineNr, charNr))
        return lexNext(rest[3:], lineNr, charNr + 4, tokens)
    elif listStartsWith(input, "え！？"):
        tokens.append(Tokens.Else(lineNr, charNr))
        return lexNext(rest[2:], lineNr, charNr + 3, tokens)
    elif listStartsWith(input, "Well Crabs let me ask you a question."):
        tokens.append(FL_Tokens.For_Loop_Opening(lineNr, charNr))
        return lexNext(rest[36:], lineNr, charNr + 37, tokens)
    elif listStartsWith(input, "If I back it up"):
        tokens.append(FL_Tokens.For_Loop_Default_Starting_Value(lineNr, charNr))
        return lexNext(rest[14:], lineNr, charNr + 15, tokens)
    elif listStartsWith(input, "If I speed it up, can "):
        tokens.append(FL_Tokens.For_Loop_Default_Increment(lineNr, charNr))
        return lexNext(rest[20:], lineNr, charNr + 21, tokens)
    elif listStartsWith(input, "If I slow it down, can "):
        tokens.append(FL_Tokens.For_Loop_Default_Decrement(lineNr, charNr))
        return lexNext(rest[21:], lineNr, charNr + 22, tokens)
    elif listStartsWith(input, "If I "):
        tokens.append(FL_Tokens.For_Loop_Starting_Value_Definition_Or_Increment_Definition(lineNr, charNr))
        return lexNext(rest[3:], lineNr, charNr + 4, tokens)
    elif listStartsWith(input, ", is it "):
        tokens.append(FL_Tokens.For_Loop_Comparison_Operator_Definition(lineNr, charNr))
        return lexNext(rest[6:], lineNr, charNr + 7, tokens)
    elif listStartsWith(input, "enough?"):
        tokens.append(FL_Tokens.For_Loop_Comparison_Operator_Definition_End(lineNr, charNr))
        return lexNext(rest[6:], lineNr, charNr + 7, tokens)
    elif listStartsWith(input, "When I throw it back, is "):
        tokens.append(FL_Tokens.For_Loop_Body_Definition(lineNr, charNr))
        return lexNext(rest[23:], lineNr, charNr + 24, tokens)
    elif listStartsWith(input, "fast enough?"):
        tokens.append(FL_Tokens.For_Loop_Body_Definition_End(lineNr, charNr))
        return lexNext(rest[11:], lineNr, charNr + 12, tokens)
    elif listStartsWith(input, "it up, can "):
        tokens.append(FL_Tokens.For_Loop_Increment_Definition_End(lineNr, charNr))
        return lexNext(rest[9:], lineNr, charNr + 10, tokens)
    elif listStartsWith(input, "handle that?"):
        tokens.append(FL_Tokens.For_Loop_Control_Value_Definition_End(lineNr, charNr))
        return lexNext(rest[11:], lineNr, charNr + 12, tokens)
    elif listStartsWith(input, "tHe fOrMuLA"):
        tokens.append(FL_Tokens.For_Loop_End(lineNr, charNr))
        return lexNext(rest[10:], lineNr, charNr + 11, tokens)
    else:
        return lexIdentifier(input, lineNr, charNr, tokens)
    return lexNext(rest, lineNr, charNr + 1, tokens)

# lex :: String -> List[Token]
def lex(inputFilePath : str) -> List[Tokens.Token]:
    input = readFile(inputFilePath)
    return lexNext(list(input), 1, 1, [])

for token in lex("input/test-subroutines.sadge"):
    print(token)