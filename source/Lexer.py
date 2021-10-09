from typing import Callable, List, TypeVar
import Tokens
import For_Loop_Tokens as FL_Tokens
import KeywordCollections as KC
from functools import reduce
from utilities import zipWith, timer, unknownError

# readFile :: String -> String
def readFile(inputFilePath : str) -> str:
    with open(inputFilePath, "r", encoding="utf8") as inputFile: # utf8 encoding is required for the hiraga, kanji, etc.
        return inputFile.read() 

# listStartsWith :: [String] -> [String] -> Bool
def listStartsWith(list1 : List[str], list2 : List[str]) -> bool:
    '''Returns True if the first list starts with, and fully contains, the second.'''
    return reduce(lambda bool1, bool2: bool1 and bool2, zipWith(lambda char1, char2: char1 == char2, list1, list2), True)

# findMapped :: [String] -> [String] -> Boolean -> [String] -> [String] -> Integer -> Integer
def findMapped(f : Callable[[List[str], List[str]], bool], list1 : List[str], list2 : List[str], depth : int=0) -> int:
    '''Returns the index where the function first evaluated to true. The function is called for every item in list2 as f(list1, item).'''
    if len(list2) <= 0:
        return -1
    head, *tail = list2
    if f(list1, list(head)):
        return depth
    else:
        return findMapped(f, list1, tail, depth+1)

# lexNext :: [Char] -> Integer -> Integer -> [Token] -> String -> Integer -> [Token]
def lexInt(input : List[str], lineNr : int, charNr : int, tokens : List[Tokens.Token], number : str='', value : int=0) -> List[Tokens.Token]:
    '''Returns the token list with a new fully lexed int appended, or ends on an error. The README contains more information about how ints work in sadge.'''
    if len(input) <= 0:
        if KC.integers[number[-1]] in range(1,10): # If the last character was a normal number (1-9) we still need to add it our total
            tokens.append(Tokens.Integer(lineNr, charNr-len(number), value + KC.integers[number[-1]]))
        else:   # If it was one of the magnifier (10, 100, 1000, etc) we've already got the correct total, so we just make the token as is
            tokens.append(Tokens.Integer(lineNr, charNr-len(number), value))
        return tokens
    char, *rest = input
    if char == '\n':
        # newline in number error
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    if char not in KC.integers: # The character is no longer (part of) a number, so we want to end our lexing
        if KC.integers[number[-1]] in range(1,10): # If the last character was a normal number (1-9) we still need to add it our total
            tokens.append(Tokens.Integer(lineNr, charNr-len(number), value + KC.integers[number[-1]]))
            return lexNext(input, lineNr, charNr, tokens)
        else: # If it was one of the magnifier (10, 100, 1000, etc) we've already got the correct total, so we just make the token as is
            tokens.append(Tokens.Integer(lineNr, charNr-len(number), value))
            return lexNext(input, lineNr, charNr, tokens)
    else:
        n = KC.integers[char] # Grab the value of the char
        if n in range(1,10): # If its a normal number (1-9)
            if len(number)<=0: # If its the first digit we just add the char to our number string so we can potentially multiply it by a magnifier next loop, or add it to the value if there is no multiplier
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value)
            elif KC.integers[number[-1]] in range(1,10): # If the previous was also a normal number thats an error.
                print(f"[Lexer] Syntax Error: Number attached to other number without spacing at line {lineNr}, char {charNr}.")
                tokens.append(Tokens.Integer(lineNr, charNr-len(number), value + KC.integers[number[-1]]))
                return lexNext(input, lineNr, charNr, tokens)
            else: # If the previous was a magnifier we just add the char to our number string so we can potentially multiply it by a magnifier next loop, or add it to the value if there is no multiplier
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value)
        else: # Char must be a magnifier
            if len(number)<=0: # If its the first digit we add it to the value and continue lexing
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value + n)
            elif KC.integers[number[-1]] in range(1,10): # If the previous was a normal number, we multiply the two so as to apply the magnification
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value + (n * KC.integers[number[-1]]))
            else: # If the previous was also a magnifier, we add it to the value and continue lexing
                return lexInt(rest, lineNr, charNr + 1, tokens, number + char, value + n)

# lexNext :: [Char] -> Integer -> Integer -> [Token] -> String -> [Token]
def lexIdentifier(input : List[str], lineNr : int, charNr : int, tokens : List[Tokens.Token], name : str='') -> List[Tokens.Token]:
    '''Returns the token list with a fully lexed identifier appended. Keeps going until it finds an honorific.'''
    if len(input) <= 0: # If the file ends mid-identifier thats an error
        print(f"[Lexer] Unexpected end of file at line {lineNr}, char {charNr}.")
        return tokens
    char, *rest = input
    if char == '\n': # Ignore \n
        return lexIdentifier(rest, lineNr + 1, 1, tokens, name)
    else:
        index = findMapped(listStartsWith, input, KC.honorifics) # Find the honorific
        if index >= 0: # If an honorific was found
            tokens.append(Tokens.Identifier(lineNr, charNr-len(name), name + KC.honorifics[index])) # Make identifier token with the lexed name + the identifier, the charNr we want is the start of the identifier, thats why we charNr-len(name).
            return lexNext(rest[len(KC.honorifics[index])-1:], lineNr, charNr+len(KC.honorifics[index]), tokens)
    return lexIdentifier(rest, lineNr, charNr + 1, tokens, name + char) # Add char to name and keep going    

# lexNext :: [Char] -> Integer -> Integer -> [Token] -> [Token]
def lexNext(input : List[str], lineNr : int, charNr : int, tokens : List[Tokens.Token]) -> List[Tokens.Token]:
    '''Returns the fully lexed result of input. Pass both lineNr and charNr as 1 initially.'''
    if len(input) <= 0:
        return tokens
    char, *rest = input
    if char == '\n':                                # We look at all the single character tokens first.
        return lexNext(rest, lineNr + 1, 1, tokens) # These could also be done with the method for longer
    elif char == ' ': # Ignore spaces               # tokens, which would make them easier to change.
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
    elif char == '。':
        tokens.append(Tokens.Parameter_Seperator(lineNr, charNr))
    elif char == '【':
        tokens.append(Tokens.Expression_Bracket_Open(lineNr, charNr))
    elif char == '】':
        tokens.append(Tokens.Expression_Bracket_Close(lineNr, charNr))
    elif listStartsWith(input, ">="):                                   # This is where we start looking at the longer tokens.
        tokens.append(Tokens.Greater_Than_Or_Equal(lineNr, charNr))     # We simply append the one we find and then keep going after.
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
    elif listStartsWith(input, "yabe!"):
        tokens.append(Tokens.Print_Statement(lineNr, charNr))
        return lexNext(rest[4:], lineNr, charNr + 5, tokens)
    elif listStartsWith(input, "yabe"):
        tokens.append(Tokens.Print_Statement(lineNr, charNr))
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
        return lexIdentifier(input, lineNr, charNr, tokens) # If it's not any preset token, it must be an identifier!
    return lexNext(rest, lineNr, charNr + 1, tokens) # Default continue for single char

# lex :: String -> [Token]
@timer
def lex(inputFilePath : str) -> List[Tokens.Token]:
    '''Returns the result of lexing the input file, or stops at an error. Has a .time attribute containing the time it took to run the function.'''
    input = readFile(inputFilePath)
    return lexNext(list(input), 1, 1, [])