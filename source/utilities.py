from io import TextIOWrapper
from typing import Callable, List, TypeVar, Union, Tuple
import inspect
from KeywordCollections import honorifics, romajiHonorifics
from functools import wraps
import time

# unkownError :: String -> None
def unknownError(pythonFilename : str):
    print(f"Exited due to unhandled error at line {inspect.currentframe().f_back.f_lineno} in file {pythonFilename}")
    exit(69)

                   #(as in, a writable opened file)
# unknownCompilerError :: file -> String -> None
def unknownCompilerError(outputFile : TextIOWrapper, pythonFilename : str):
    outputFile.write(f"Exited due to unhandled error at line {inspect.currentframe().f_back.f_lineno} in file {pythonFilename}")
    outputFile.close()
    print(f"Exited due to unhandled error at line {inspect.currentframe().f_back.f_lineno} in file {pythonFilename}")
    exit(420)

# space :: Integer -> String
def space( repeatCount : int):
    if (repeatCount <= 0):
        return ""
    return "|   " + space(repeatCount - 1) # I chose to define the actual string spaces here so that I can change it in a single place if I ever want to.

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
# zipWith :: (a → b → c) → [a] → [b] → [c]
def zipWith(f : Callable[[A, B], C], xs : List[A], ys : List[B]) -> List[C]:
    if len(xs) == 0 or len(ys) == 0:
        return [] # Stop when either list is empty
    else:
        x, *xrest = xs # Split head x of list xs
        y, *yrest = ys # Split head y of list ys
        return [f(x,y)] + zipWith(f, xrest, yrest) # Recursion:
        # apply f to x and y, then concatenate to f applied to rest

A = TypeVar('A')
B = TypeVar('B')
# find :: (a → b → Bool) → [a] → b → Int
def find(f : Callable[[A, B], bool], list : List[A], target : B, index=0) -> int:
    '''Returns the index of the item in list where the function evaluates to true. Or None, if that never happens.'''
    if len(list) == 0:
        return None
    item, *rest = list
    if f(item, target):
        return index
    else:
        return find(f, rest, target, index + 1)

# stripHonorific :: String -> String
def stripHonorific(input : str) -> str:
    '''Removes any honorific of the given string.'''
    return stripHonorificRecursion(input, input)

# stringHonorificRecursion :: String -> String -> String
def stripHonorificRecursion(input : str, honorific : str) -> str:
    if len(honorific) <= 0:
        return None
    elif honorific in honorifics:
        return input[:len(input)-len(honorific)]
    else:
        return stripHonorificRecursion(input, honorific[1:])

def timer(f : Callable) -> Callable:
    '''A Decorator that times how long it takes to run the decorated function.'''
    @wraps(f)
    def inner(*args, **kwargs):
        inner.time = time.time()
        result = f(*args, **kwargs)
        inner.time = time.time() - inner.time
        return result
    return inner

# stringEndsWithAnyOf :: String -> [String] -> String | None
def stringEndsWithAnyOf(input : str, endings : List[str]) -> Union[str, None]:
    '''Checks if the input string ends with any of the listed endings, if so returns that ending, otherwise returns None.'''
    if len(endings) <= 0:
        return None
    else:
        ending, *rest = endings
        if input.endswith(ending):
            return ending
        else:
            return stringEndsWithAnyOf(input, rest)

# parseRuntimeOptions :: str -> [char] -> [char]
def parseRuntimeOptions(options : str, parsedOptions : List[str]) -> List[str]:
    '''Parses a string of options like: "-ILP", returns a list of those characters seperated out. No support for specific values, only; the option is there, or it is not.'''
    if len(options) <= 0:
        return parsedOptions
    option, *rest = options
    parsedOptions.append(option)
    return parseRuntimeOptions(rest, parsedOptions)

# parseRuntimeArguments :: [String] -> [String] -> ([String], [String])'
def parseRuntimeArguments(arguments : List[str], parsedArgs : List[str]) -> Tuple[List[str], List[str]]:
    '''Parses a list of strings containing the runtime arguments. Returns a tuple containing a list of arguments to be passed to the interpreter and a list of options passed like; "-ILP".'''
    if len(arguments) <= 0:
        return parsedArgs, []
    argument, *rest = arguments
    if argument.startswith('-'):
        return parsedArgs, parseRuntimeOptions(argument, [])
    else:
        if argument.isdigit():
            argument = int(argument)
        parsedArgs.append(argument)
        return parseRuntimeArguments(rest, parsedArgs)

# romajifyHonorific :: String -> String
def romajifyHonorific(input : str) -> str:
    '''Changes any honorific of the given string to romaji.'''
    return romajifyHonorificRecursion(input, input)

# romajifyHonorificRecursion :: String -> String -> String
def romajifyHonorificRecursion(input : str, honorific : str) -> str:
    if len(honorific) <= 0:
        return None
    elif honorific in honorifics:
        return input[:len(input)-len(honorific)] + '_' + romajiHonorifics[honorific]
    else:
        return romajifyHonorificRecursion(input, honorific[1:])
