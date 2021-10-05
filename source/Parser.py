import functools
import AST_classes as ASTc
from typing import List, Tuple, Union
import Tokens
import Token_Patterns as TP
from utilities import unknownError, zipWith
from functools import reduce

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
# parseParameterList :: List[Tokens.Token] -> ASTc.Parameter_List -> Int ->Tuple[, List[Tokens.Token], ASTc.Parameter_List]
def parseParameterList(tokens : List[Tokens.Token], parameterList : ASTc.Parameter_List, nestLevel : int) -> Tuple[List[Tokens.Token], ASTc.Parameter_List]:
    if len(tokens) <= 0:
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if isinstance(token, Tokens.Parameter_List_Close):
        return rest, parameterList
    elif checkForPattern(tokens, TP.Parameter_List_Last_Item):
        parameterList.append(token)
        return rest[len(TP.Parameter_List_Last_Item)-1:], parameterList
    elif checkForPattern(tokens, TP.Parameter_List_Item):
        parameterList.append(token)
        return parseParameterList(rest[len(TP.Parameter_List_Item)-1:], parameterList, nestLevel)
    else:
        print(f"Parameter List Syntax Error at {token.lineNr}, {token.charNr} or {rest[0].lineNr}, {rest[0].charNr}")
        return tokens, None

def parseExpression(tokens : List[Tokens.Token], expression : ASTc.Expression, nestLevel : int) -> Tuple[List[Tokens.Token], Union[ASTc.Expression, Tokens.Value]]:
    if len(tokens) <= 0:
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if expression.left == None:
        if isinstance(token, Tokens.Expression_Bracket_Open):
            rest, expression.left = parseExpression(rest, ASTc.Expression(nestLevel + 1), nestLevel+1)
            token, *rest = rest
            if not isinstance(token, Tokens.Expression_Bracket_Close):
                #TODO: ADD ERROR HANDLING
                unknownError(__file__)
        elif checkForPattern(tokens, TP.Function_Call):
            rest, expression.left = parseFunctionCall(tokens[len(TP.Function_Call):], ASTc.Function_Call(nestLevel + 1, tokens[TP.Function_Call.index(Tokens.Identifier)]), nestLevel+1)
        elif isinstance(token, Tokens.Value):
            expression.left = token
        else:
            #TODO: ADD ERROR HANDLING
            print(token)
            unknownError(__file__)
        return parseExpression(rest, expression, nestLevel)
    elif expression.operator == None:
        if isinstance(token, Tokens.Operator):
            expression.operator = token
            return parseExpression(rest, expression, nestLevel)
        else:
            return tokens, expression.left
    elif expression.right == None:
        if isinstance(token, Tokens.Expression_Bracket_Open):
            rest, expression.right = parseExpression(rest, ASTc.Expression(nestLevel + 1), nestLevel+1)
            token, *rest = rest
            if not isinstance(token, Tokens.Expression_Bracket_Close):
                #TODO: ADD ERROR HANDLING
                unknownError(__file__)
            else:
                return parseExpression(rest, expression, nestLevel)
        elif checkForPattern(tokens, TP.Function_Call):
            rest, expression.left = parseFunctionCall(tokens[len(TP.Function_Call):], ASTc.Function_Call(nestLevel + 1, tokens[TP.Function_Call.index(Tokens.Identifier)]), nestLevel+1)
        elif isinstance(token, Tokens.Value):
            expression.right = token
        else:
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)
        return parseExpression(rest, expression, nestLevel)
    else:
        if isinstance(token, Tokens.Operator):
            newExpression = ASTc.Expression(nestLevel + 1, expression, token)
            return parseExpression(rest, newExpression, nestLevel)
        else:
            return tokens, expression

def parseFunctionCall(tokens : List[Tokens.Token], functionCall : ASTc.Function_Call, nestLevel : int) -> Tuple[List[Tokens.Token], ASTc.Function_Call]:
    if len(tokens) <= 0:
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if checkForPattern(tokens, TP.Function_Call) or isinstance(token, Tokens.Value) or isinstance(token, Tokens.Expression_Bracket_Open):
        rest, parameter = parseExpression(tokens, ASTc.Expression(nestLevel + 1), nestLevel+1)
    else:
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = rest
    if isinstance(token, Tokens.Parameter_Seperator):
        if functionCall.parameterList == None:
            functionCall.parameterList = ASTc.Parameter_List(nestLevel + 1)
        functionCall.parameterList.append(parameter)
        return parseFunctionCall(rest, functionCall, nestLevel)
    elif isinstance(token, Tokens.Parameter_List_Close):
        if functionCall.parameterList == None:
            functionCall.parameterList = ASTc.Parameter_List(nestLevel + 1)
        functionCall.parameterList.append(parameter)
        return rest, functionCall
    else:
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)

def parseForLoop(tokens : List[Tokens.Token], forLoop : ASTc.For_Loop, nestLevel : int) -> Tuple[List[Tokens.Token], ASTc.For_Loop]:
    if len(tokens) <= 0:
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if forLoop.startingValue == None:
        if checkForPattern(tokens, TP.For_Loop_Opening):
            rest = tokens[len(TP.For_Loop_Opening):]
            if checkForPattern(rest, TP.For_Loop_Default_Starting_Value):
                forLoop.startingValue = 1
                return parseForLoop(rest[len(TP.For_Loop_Default_Starting_Value):], forLoop, nestLevel)
            elif checkForPattern(rest, TP.For_Loop_Starting_Value_Definition):
                rest = rest[len(TP.For_Loop_Starting_Value_Definition):]
                rest, expression = parseExpression(rest, ASTc.Expression(nestLevel + 1), nestLevel+1)
                if checkForPattern(rest, TP.For_Loop_Starting_Value_Definition_End):
                    rest = rest[len(TP.For_Loop_Starting_Value_Definition_End):]
                    forLoop.startingValue = expression
                    return parseForLoop(rest, forLoop, nestLevel)
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    elif forLoop.comparisonOperator == None:
        if isinstance(token, Tokens.Logic_Operator):
            forLoop.comparisonOperator = token
            return parseForLoop(rest, forLoop, nestLevel)
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    elif forLoop.body == None:
        if checkForPattern(tokens, TP.For_Loop_Body_Definition):
            rest, codeBlock = parseCodeBlock(tokens[len(TP.For_Loop_Body_Definition):], ASTc.Code_Block(nestLevel + 1), nestLevel+1)
            if checkForPattern(rest, TP.For_Loop_Body_Definition_End):
                forLoop.body = codeBlock
                return parseForLoop(rest[len(TP.For_Loop_Body_Definition_End):], forLoop, nestLevel)
        #TODO: ADD ERROR HANDLING
        print(rest[1])
        unknownError(__file__)
    elif forLoop.increment == None:
        if checkForPattern(tokens, TP.For_Loop_Default_Increment):
            forLoop.increment = 1
            return parseForLoop(tokens[len(TP.For_Loop_Default_Increment):], forLoop, nestLevel)
        elif checkForPattern(tokens, TP.For_Loop_Default_Decrement):
            forLoop.increment = -1
            return parseForLoop(tokens[len(TP.For_Loop_Default_Decrement):], forLoop, nestLevel)
        elif checkForPattern(tokens, TP.For_Loop_Increment_Definition):
            rest, expression = parseExpression(tokens[len(TP.For_Loop_Increment_Definition):], ASTc.Expression(nestLevel + 1), nestLevel+1)
            forLoop.increment = expression
            return parseForLoop(rest, forLoop)
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    elif forLoop.controlValue == None:
        if isinstance(token, Tokens.Value) or isinstance(token, Tokens.Expression_Bracket_Open):
            rest, expression = parseExpression(tokens, ASTc.Expression(nestLevel + 1), nestLevel+1)
            if checkForPattern(rest, TP.For_Loop_End):
                forLoop.controlValue = expression
                return rest[len(TP.For_Loop_End):], forLoop
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    #TODO: ADD ERROR HANDLING
    unknownError(__file__)

def parseCodeBlock(tokens : List[Tokens.Token], codeBlock : ASTc.Code_Block, nestLevel : int) -> Tuple[List[Tokens.Token], ASTc.Code_Block]:
    if len(tokens) <= 0:
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if isinstance(token, Tokens.Code_Block_Close):
        return rest, codeBlock
    elif checkForPattern(tokens, TP.Function_Call):
        rest, functionCall = parseFunctionCall(tokens[len(TP.Function_Call):], ASTc.Function_Call(nestLevel + 1, tokens[TP.Function_Call.index(Tokens.Identifier)]), nestLevel+1)
        token, *rest = rest
        if isinstance(token, Tokens.Endline):
            codeBlock.append(functionCall)
            return parseCodeBlock(rest, codeBlock, nestLevel)
        else:
            # Missing endline error
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)
    elif isinstance(token, Tokens.Return_Statement):
        rest, returnItem = parseExpression(rest, ASTc.Expression(nestLevel + 1), nestLevel+1)
        token, *rest = rest
        if isinstance(token, Tokens.Endline):
            codeBlock.append(ASTc.Return_Statement(nestLevel + 1, returnItem))
            return parseCodeBlock(rest, codeBlock, nestLevel)
        else:
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)
    elif isinstance(token, Tokens.Print_Statement):
        rest, returnItem = parseExpression(rest, ASTc.Expression(nestLevel + 1), nestLevel+1)
        token, *rest = rest
        if isinstance(token, Tokens.Endline):
            codeBlock.append(ASTc.Print_Statement(nestLevel + 1, returnItem))
            return parseCodeBlock(rest, codeBlock, nestLevel)
        else:
            print(token)
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)
    elif checkForPattern(tokens, TP.Assignment_Or_If_Statement):
        identifier = token
        rest, expression = parseExpression(tokens[len(TP.Assignment_Or_If_Statement):], ASTc.Expression(nestLevel + 1), nestLevel+1)
        if checkForPattern(rest, TP.If_Statement_End):
            rest, trueCodeBlock = parseCodeBlock(rest[len(TP.If_Statement_End):], ASTc.Code_Block(nestLevel + 2), nestLevel+2)
            elseCodeBlock = None
            if checkForPattern(rest, TP.Else):
                rest, elseCodeBlock = parseCodeBlock(rest[len(TP.Else):], ASTc.Code_Block(nestLevel + 2), nestLevel+2)
            codeBlock.append(ASTc.If_Statement(nestLevel + 1, identifier, expression, trueCodeBlock, elseCodeBlock))
        elif checkForPattern(rest, TP.Assignment_End):
            codeBlock.append(ASTc.Variable_Assignment(nestLevel + 1, identifier, expression))
            rest = rest[len(TP.Assignment_End):]
        else:
            #TODO: ADD ERROR HANDLING
            print(expression)
            unknownError(__file__)
        return parseCodeBlock(rest, codeBlock, nestLevel)
    elif checkForPattern(tokens, TP.For_Loop_Opening):
        rest, forLoop = parseForLoop(tokens, ASTc.For_Loop(nestLevel + 1), nestLevel+1)
        codeBlock.append(forLoop)
        return parseCodeBlock(rest, codeBlock, nestLevel)
    #TODO: ADD ERROR HANDLING
    print(token)
    unknownError(__file__)

def parseNext(tokens : List[Tokens.Token], ASTs : List[ASTc.AST], nestLevel : int) -> List[ASTc.AST]:
    if len(tokens) <= 0:
        return ASTs
    token, *rest = tokens
    if checkForPattern(tokens, TP.Function_Definition_Start):
        identifier = tokens[TP.Function_Definition_Start.index(Tokens.Identifier)]
        tokens, parameterList = parseParameterList(rest[2:], ASTc.Parameter_List(nestLevel + 1), nestLevel + 1)
        token, *rest = tokens
        if isinstance(token, Tokens.Endline):
            ASTs.append(ASTc.AST(nestLevel, identifier, parameterList))
            return parseNext(rest, ASTs, nestLevel)
        elif isinstance(token, Tokens.Code_Block_Open):
            rest, codeBlock = parseCodeBlock(rest, ASTc.Code_Block(nestLevel + 1), nestLevel + 1)
            ASTs.append(ASTc.AST(nestLevel, identifier, parameterList, codeBlock))
            return parseNext(rest, ASTs, nestLevel)
        else:
            print(f"Expected Endline or Code_Block_Open at {token.lineNr}, {token.charNr}. Got {type(token)}")
    else:
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)

def compareIdentifierNames(id1 : Tokens.Identifier, id2 : Tokens.Identifier) -> bool:
    print(f"id1: {str(id1)}\nid2: {str(id2)}")
    return id1.name == id2.name

def compareParameterList(list1 : ASTc.Parameter_List, list2 : ASTc.Parameter_List) -> bool:
    if len(list1.values) != len(list2.values):
        return False
    else:
        return reduce(lambda bool1, bool2: bool1 and bool2, zipWith(compareIdentifierNames, list1.values, list2.values), True)

def squashASTList(ASTs : List[ASTc.AST], namesFound : dict[str, int]=dict(), squashedASTList : List[ASTc.AST]=[]) -> List[ASTc.AST]:
    if len(ASTs) <= 0:
        return squashedASTList
    ast, *rest = ASTs
    if ast.identifier.name in namesFound:
        if compareParameterList(squashedASTList[namesFound[ast.identifier.name]].parameterList, ast.parameterList):
            if squashedASTList[namesFound[ast.identifier.name]].codeBlock == None:
                squashedASTList[namesFound[ast.identifier.name]].codeBlock = ast.codeBlock
                return squashASTList(rest, namesFound, squashedASTList)
            else:
                # redefinition error
                #TODO: ADD ERROR HANDLING
                unknownError(__file__)
    namesFound[ast.identifier.name] = len(squashedASTList)
    squashedASTList.append(ast)
    return squashASTList(rest, namesFound, squashedASTList)

def checkForMissingImplementations(ASTs : List[ASTc.AST], ASTsWithImplementations : List[ASTc.AST]=[]) -> List[ASTc.AST]:
    if len(ASTs) <= 0:
        return ASTsWithImplementations
    ast, *rest = ASTs
    if ast.codeBlock == None:
        # missing implementation error
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    else:
        ASTsWithImplementations.append(ast)
        return checkForMissingImplementations(rest, ASTsWithImplementations)

def parse(tokens : List[Tokens.Token]) -> List[ASTc.AST]:
    ASTs = parseNext(tokens, [], 1)
    # print(f"Constructed {len(ASTs)} ASTs.\n")
    # for ast in ASTs:
    #     print(ast)
    ASTs = squashASTList(ASTs)
    ASTs = checkForMissingImplementations(ASTs)
    return ASTs
