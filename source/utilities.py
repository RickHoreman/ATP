from typing import Callable, List, TypeVar
import inspect
from KeywordCollections import honorifics
from functools import wraps
import time

# unkownError :: String -> None
def unknownError(filename : str):
    print(f"Exited due to unhandled error at line {inspect.currentframe().f_back.f_lineno} in file {filename}")
    exit(69) 

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