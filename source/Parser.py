import AST_classes as ASTc
from typing import Callable, List, Tuple
import Tokens
import Token_Patterns as TP
from source.Tokens import Code_Block_Open

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

# parseParameterList :: List[Tokens.Token] -> ASTc.Parameter_List -> ASTc.Parameter_List
def parseParameterList(tokens : List[Tokens.Token], parameterList : ASTc.Parameter_List) -> Tuple[List[Tokens.Token], ASTc.Parameter_List]:
    if len(tokens) <= 0:
        # ADD ERROR HANDLING
        return tokens, None
    token, *rest = tokens
    if checkForPattern(tokens, TP.Parameter_List_Last_Item):
        print("Parameter List End")
        parameterList.append(token)
        return rest[1:], parameterList
    elif checkForPattern(tokens, TP.Parameter_List_Item):
        print("Parameter List Item")
        parameterList.append(token)
        return parameterList(tokens, parameterList)
    else:
        print("Parameter List Ended Prematurely") # ADD PROPER ERROR HANDLING
        return tokens, None

def parseCodeBlock(tokens : List[Tokens.Token], codeBlock : ASTc.Code_Block) -> ASTc.Code_Block:
    if len(tokens) <= 0:
        return codeBlock

def parseNext(tokens : List[Tokens.Token], ASTs : List[ASTc.AST]=[]) -> List[ASTc.AST]:
    if len(tokens) <= 0:
        return ASTs
    elif len(ASTs) <= 0:
        ASTs.append(ASTc.AST())
    token, *rest = tokens
    if checkForPattern(tokens, TP.Integer_Assignment):
        ASTs[-1].codeBlock.append(ASTc.Assignment(tokens[0].name, tokens[2].value))
        return parseNext(tokens[len(TP.Integer_Assignment):], ASTs)
    elif checkForPattern(tokens, TP.Function_Definition_Start):
        tokens, parameterList = parseParameterList(rest[2:], ASTc.Parameter_List())
        token, *rest = tokens
        if isinstance(token, Tokens.Endline):
            dunno
        elif isinstance(token, Tokens.Code_Block_Open):
            
        else:
            print(f"Syntax error at {token.lineNr}, {token.charNr}")

    

def parse(tokens : List[Tokens.Token]) -> List[ASTc.AST]:
    return parseNext(tokens)