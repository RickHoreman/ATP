import AST_classes as ASTc
from typing import List, Tuple, Union
import Tokens
import Token_Patterns as TP
from utilities import unknownError

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

#Specifically for function defintions!
# parseParameterList :: List[Tokens.Token] -> ASTc.Parameter_List -> ASTc.Parameter_List
def parseParameterList(tokens : List[Tokens.Token], parameterList : ASTc.Parameter_List) -> Tuple[List[Tokens.Token], ASTc.Parameter_List]:
    if len(tokens) <= 0:
        # ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if isinstance(token, Tokens.Parameter_List_Close):
        return rest, parameterList
    elif checkForPattern(tokens, TP.Parameter_List_Last_Item):
        parameterList.append(token)
        return rest[len(TP.Parameter_List_Last_Item)-1:], parameterList
    elif checkForPattern(tokens, TP.Parameter_List_Item):
        parameterList.append(token)
        return parseParameterList(rest[len(TP.Parameter_List_Item)-1:], parameterList)
    else:
        print(f"Parameter List Syntax Error at {token.lineNr}, {token.charNr} or {rest[0].lineNr}, {rest[0].charNr}")
        return tokens, None

def parseExpression(tokens : List[Tokens.Token], expression : ASTc.Expression) -> Tuple[List[Tokens.Token], Union[ASTc.Expression, Tokens.Value]]:
    if len(tokens) <= 0:
        # ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if expression.left == None:
        if isinstance(token, Tokens.Expression_Bracket_Open):
            rest, expression.left = parseExpression(rest, ASTc.Expression())
            token, *rest = rest
            if not isinstance(token, Tokens.Expression_Bracket_Close):
                # ADD ERROR HANDLING
                unknownError(__file__)
        elif isinstance(token, Tokens.Value):
            expression.left = token
        else:
            # ADD ERROR HANDLING
            print(token)
            unknownError(__file__)
        return parseExpression(rest, expression)
    elif expression.operator == None:
        if isinstance(token, Tokens.Operator):
            expression.operator = token
            return parseExpression(rest, expression)
        else:
            return tokens, expression.left
    elif expression.right == None:
        if isinstance(token, Tokens.Expression_Bracket_Open):
            rest, expression.right = parseExpression(rest, ASTc.Expression())
            token, *rest = rest
            if not isinstance(token, Tokens.Expression_Bracket_Close):
                # ADD ERROR HANDLING
                unknownError(__file__)
            else:
                return parseExpression(rest, expression)
        elif isinstance(token, Tokens.Value):
            expression.right = token
        else:
            # ADD ERROR HANDLING
            unknownError(__file__)
        return parseExpression(rest, expression)
    else:
        if isinstance(token, Tokens.Operator):
            newExpression = ASTc.Expression(expression, token)
            return parseExpression(rest, newExpression)
        else:
            return tokens, expression

def parseFunctionCall(tokens : List[Tokens.Token], functionCall : ASTc.Function_Call) -> Tuple[List[Tokens.Token], ASTc.Function_Call]:
    if len(tokens) <= 0:
        # ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if checkForPattern(tokens, TP.Function_Call):
        rest, parameter = parseFunctionCall(tokens[len(TP.Function_Call):], ASTc.Function_Call(tokens[TP.Function_Call.index(Tokens.Identifier)]))
    elif isinstance(token, Tokens.Value) or isinstance(token, Tokens.Expression_Bracket_Open):
        rest, parameter = parseExpression(tokens, ASTc.Expression())
    else:
        # ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = rest
    if isinstance(token, Tokens.Parameter_Seperator):
        if functionCall.parameterList == None:
            functionCall.parameterList = ASTc.Parameter_List()
        functionCall.parameterList.append(parameter)
        return parseFunctionCall(rest, functionCall)
    elif isinstance(token, Tokens.Parameter_List_Close):
        if functionCall.parameterList == None:
            functionCall.parameterList = ASTc.Parameter_List()
        functionCall.parameterList.append(parameter)
        return rest, functionCall
    else:
        # ADD ERROR HANDLING
        unknownError(__file__)

def parseCodeBlock(tokens : List[Tokens.Token], codeBlock : ASTc.Code_Block) -> Tuple[List[Tokens.Token], ASTc.Code_Block]:
    if len(tokens) <= 0:
        # ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if isinstance(token, Tokens.Code_Block_Close):
        return rest, codeBlock
    elif isinstance(token, Tokens.Return_Statement):
        if checkForPattern(rest, TP.Function_Call):
            rest, returnItem = parseFunctionCall(rest[len(TP.Function_Call):], ASTc.Function_Call(rest[TP.Function_Call.index(Tokens.Identifier)]))
        else:
            rest, returnItem = parseExpression(rest, ASTc.Expression())
        token, *rest = rest
        if isinstance(token, Tokens.Endline):
            codeBlock.append(ASTc.Return_Statement(returnItem))
            return parseCodeBlock(rest, codeBlock)
        else:
            # ADD ERROR HANDLING
            unknownError(__file__)
    elif checkForPattern(tokens, TP.Assignment_Or_If_Statement):
        identifier = token
        rest, expression = parseExpression(tokens[len(TP.Assignment_Or_If_Statement):], ASTc.Expression())
        if checkForPattern(rest, TP.If_Statement_End):
            rest, trueCodeBlock = parseCodeBlock(rest[len(TP.If_Statement_End):], ASTc.Code_Block())
            elseCodeBlock = None
            if checkForPattern(rest, TP.Else):
                rest, elseCodeBlock = parseCodeBlock(rest[len(TP.Else):], ASTc.Code_Block())
                codeBlock.append(ASTc.If_Statement(identifier, expression, trueCodeBlock))
            codeBlock.append(ASTc.If_Statement(identifier, expression, trueCodeBlock, elseCodeBlock))
        elif checkForPattern(rest, TP.Assignment_End):
            codeBlock.append(ASTc.Variable_Assignment(identifier, expression))
            rest = rest[len(TP.Assignment_End):]
        else:
            # ADD ERROR HANDLING
            unknownError(__file__)
        return parseCodeBlock(rest, codeBlock)
    # ADD ERROR HANDLING
    print(token)
    unknownError(__file__)

def parseNext(tokens : List[Tokens.Token], ASTs : List[ASTc.AST]=[]) -> List[ASTc.AST]:
    if len(tokens) <= 0:
        return ASTs
    # elif len(ASTs) <= 0:
    #     ASTs.append(ASTc.AST())
    token, *rest = tokens
    if checkForPattern(tokens, TP.Function_Definition_Start):
        identifier = tokens[TP.Function_Definition_Start.index(Tokens.Identifier)]
        tokens, parameterList = parseParameterList(rest[2:], ASTc.Parameter_List())
        token, *rest = tokens
        if isinstance(token, Tokens.Endline):
            ASTs.append(ASTc.AST(identifier, parameterList))
            return parseNext(rest, ASTs)
        elif isinstance(token, Tokens.Code_Block_Open):
            rest, codeBlock = parseCodeBlock(rest, ASTc.Code_Block())
            ASTs.append(ASTc.AST(identifier, parameterList, codeBlock))
            return parseNext(rest, ASTs)
        else:
            print(f"Expected Endline or Code_Block_Open at {token.lineNr}, {token.charNr}. Got {type(token)}")
    else:
        # ADD ERROR HANDLING
        unknownError(__file__)

def parse(tokens : List[Tokens.Token]) -> List[ASTc.AST]:
    return parseNext(tokens)