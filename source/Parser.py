import AST_classes as ASTc
from typing import Callable, List
import Tokens
import Token_Patterns as TP

# checkForPattern :: List[Tokens.Token] -> List[Tokens.Token] -> Bool
def checkForPattern(instances : List[Tokens.Token], pattern : List[Tokens.Token]) -> bool:
    if len(pattern) <= 0:
        return True
    elif len(instances) <= 0:
        return False
    instance, *instancesRest = instances
    part, *patternRest = pattern
    if not isinstance(instance, part):
        return False
    else:
        return checkForPattern(instancesRest, patternRest)

def parseNext(tokens : List[Tokens.Token], ASTs : List[ASTc.AST]=[]) -> List[ASTc.AST]:
    if len(tokens) <= 0:
        return ASTs
    elif len(ASTs) <= 0:
        ASTs.append(ASTc.AST())
    if checkForPattern(tokens, TP.Integer_Assignment):
        ASTs[-1].codeBlock.append(ASTc.Assignment(tokens[0].name, tokens[2].value))
        return parseNext(tokens[len(TP.Integer_Assignment):], ASTs)
    

def parse(tokens : List[Tokens.Token]) -> List[ASTc.AST]:
    return parseNext(tokens)