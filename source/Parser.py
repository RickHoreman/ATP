import functools
import AST_classes as ASTc
from typing import List, Tuple, Union
import Tokens
import Token_Patterns as TP
from utilities import unknownError, zipWith, timer
from functools import reduce

# checkForPattern :: List[Tokens.Token] -> List[Tokens.Token] -> Bool
def checkForPattern(instances : List[Tokens.Token], pattern : List[Tokens.Token]) -> bool:
    '''Returns true if the first list starts with the entirety of the second. Returns false if the first list runs out or if a mismatch occurs.'''
    if len(pattern) <= 0: # In this case the entire pattern matched, so we return true.
        return True
    elif len(instances) <= 0: # In this case we still have some of our pattern left to go, but the instances ran out. So no match.
        return False
    instance, *instancesRest = instances    # Take the first items
    part, *patternRest = pattern            # of both lists.
    if not isinstance(instance, part):      # Compare them.
        return False    # Mismatch
    else:
        return checkForPattern(instancesRest, patternRest) # Match next items.

# parseParameterList :: List[Tokens.Token] -> ASTc.Parameter_List -> Int ->Tuple[, List[Tokens.Token], ASTc.Parameter_List]
def parseParameterList(tokens : List[Tokens.Token], parameterList : ASTc.Parameter_List, nestLevel : int) -> Tuple[List[Tokens.Token], ASTc.Parameter_List]:
    '''Returns a tuple of the rest of the token list and a parsed parameter list. Used for parsing parameter lists on function definitions, not calls.'''
    if len(tokens) <= 0:    # We dont expect our token list to stop mid parameter list.
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if isinstance(token, Tokens.Parameter_List_Close):  # End of parameter list.
        return rest, parameterList
    elif checkForPattern(tokens, TP.Parameter_List_Last_Item):  # Also end of parameter list, but slightly different syntax.
        parameterList.append(token)
        return rest[len(TP.Parameter_List_Last_Item)-1:], parameterList # len shenanigans because we want to exclude the entire pattern we matched.
    elif checkForPattern(tokens, TP.Parameter_List_Item):   # A new item, add it, parse next.
        parameterList.append(token)
        return parseParameterList(rest[len(TP.Parameter_List_Item)-1:], parameterList, nestLevel)
    else:   # Some unexpected syntax.
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)

def parseExpression(tokens : List[Tokens.Token], expression : ASTc.Expression, nestLevel : int) -> Tuple[List[Tokens.Token], Union[ASTc.Expression, Tokens.Value]]:
    '''Returns a tuple of the rest of the token list and a parsed expression (which can be just a value).'''
    if len(tokens) <= 0:    # We dont expect our token list to run out mid expression.
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if expression.left == None: # If our parsed expression doesnt have a left side yet; parse it!
        if isinstance(token, Tokens.Expression_Bracket_Open): # This means we have a priority sub-expression that needs to be parsed first.
            rest, expression.left = parseExpression(rest, ASTc.Expression(nestLevel + 1), nestLevel+1)
            token, *rest = rest
            if not isinstance(token, Tokens.Expression_Bracket_Close): # We expected our parsed sub-expression to end
                #TODO: ADD ERROR HANDLING                              # on a closing bracket.
                unknownError(__file__)
        elif checkForPattern(tokens, TP.Function_Call): # If our expression contains a function call, we need to parse it first.
            rest, expression.left = parseFunctionCall(tokens[len(TP.Function_Call):], ASTc.Function_Call(nestLevel + 1, tokens[TP.Function_Call.index(Tokens.Identifier)]), nestLevel+1)
        elif isinstance(token, Tokens.Value): # If it's simply a value, assign it!
            expression.left = token
        else: # Some other unexpected syntax
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)
        return parseExpression(rest, expression, nestLevel) # Continue parsing our expression.
    elif expression.operator == None: # If our parsed expression doesnt have an operator yet; parse it!
        if isinstance(token, Tokens.Operator): # If it's an operator, assign and keept parsing.
            expression.operator = token
            return parseExpression(rest, expression, nestLevel)
        else:   # If it's some other token, we assume this to be then end of the expression, meaning it only has a left side.
            return tokens, expression.left  # So we return that.
    elif expression.right == None: # If our parsed expression doesnt have a right side yet; parse it!
        if isinstance(token, Tokens.Expression_Bracket_Open): # This means we have a priority sub-expression that needs to be parsed first.
            rest, expression.right = parseExpression(rest, ASTc.Expression(nestLevel + 1), nestLevel+1)
            token, *rest = rest
            if not isinstance(token, Tokens.Expression_Bracket_Close): # We expected our parsed sub-expression to end
                #TODO: ADD ERROR HANDLING                              # on a closing bracket.
                unknownError(__file__)
            else:
                return parseExpression(rest, expression, nestLevel)
        elif checkForPattern(tokens, TP.Function_Call): # If our expression contains a function call, we need to parse it first.
            rest, expression.left = parseFunctionCall(tokens[len(TP.Function_Call):], ASTc.Function_Call(nestLevel + 1, tokens[TP.Function_Call.index(Tokens.Identifier)]), nestLevel+1)
        elif isinstance(token, Tokens.Value): # If it's simply a value, assign it!
            expression.right = token
        else: # Some other unexpected syntax
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)
        return parseExpression(rest, expression, nestLevel)
    else: # If our expression has a left side, operator and right side, it is fully parsed.
        if isinstance(token, Tokens.Operator): # But in the case of 5 + 2 + 1 we also want to add the + 1, so parse a new expression, 
            newExpression = ASTc.Expression(nestLevel + 1, expression, token) # with our current expression as the left side.
            return parseExpression(rest, newExpression, nestLevel)
        else: # Otherwise, simply return our parsed expression and the tokens that come after.
            return tokens, expression

def parseFunctionCall(tokens : List[Tokens.Token], functionCall : ASTc.Function_Call, nestLevel : int) -> Tuple[List[Tokens.Token], ASTc.Function_Call]:
    '''Returns a tuple of the rest of the token list and a parsed functioncall.'''
    if len(tokens) <= 0: # We dont expect our token list to run out mid function call.
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens # tokens is the content of the brackets from the function call. We want to check if this an expression, and if so, parse the expression.
    if checkForPattern(tokens, TP.Function_Call) or isinstance(token, Tokens.Value) or isinstance(token, Tokens.Expression_Bracket_Open):
        rest, parameter = parseExpression(tokens, ASTc.Expression(nestLevel + 1), nestLevel+1)
    elif isinstance(token, Tokens.Parameter_List_Close):
        pass # If the token is a closing bracket, it must be a function call with no parameters, so pass the error.
    else: # Some other unexpected syntax.
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = rest
    if isinstance(token, Tokens.Parameter_Seperator): # Meaning we want add our parameter and parse another.
        if functionCall.parameterList == None:  # If the parameter list is still empty/doesnt exit,
            functionCall.parameterList = ASTc.Parameter_List(nestLevel + 1) # make one!
        functionCall.parameterList.append(parameter)
        return parseFunctionCall(rest, functionCall, nestLevel) # Parse next paremeter
    elif isinstance(token, Tokens.Parameter_List_Close): # End of our parameter list.
        if functionCall.parameterList == None:  # If the parameter list is still empty/doesnt exit,
            functionCall.parameterList = ASTc.Parameter_List(nestLevel + 1) # make one!
        functionCall.parameterList.append(parameter)
        return rest, functionCall
    else: # Some other unexptect syntax.
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)

def parseForLoop(tokens : List[Tokens.Token], forLoop : ASTc.For_Loop, nestLevel : int) -> Tuple[List[Tokens.Token], ASTc.For_Loop]:
    '''Returns a tuple of the rest of the token list and a parsed for loop.'''
    if len(tokens) <= 0: # We dont expect our token list to run out mid for loop.
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    token, *rest = tokens
    if forLoop.startingValue == None: # Similar structure to parseExpression; if our for loop doesnt have a starting value yet, parse it!
        if checkForPattern(tokens, TP.For_Loop_Opening): # We expect the... for loop opening line... first.
            rest = tokens[len(TP.For_Loop_Opening):] # Grab what comes after the opening.
            if checkForPattern(rest, TP.For_Loop_Default_Starting_Value): # If we get the syntax for default starting value
                forLoop.startingValue = 0                                 # set it!
                return parseForLoop(rest[len(TP.For_Loop_Default_Starting_Value):], forLoop, nestLevel)
            elif checkForPattern(rest, TP.For_Loop_Starting_Value_Definition): # If we get the syntax for a starting value definition,
                rest = rest[len(TP.For_Loop_Starting_Value_Definition):]
                rest, expression = parseExpression(rest, ASTc.Expression(nestLevel + 1), nestLevel+1) # parse the value (expression)
                if checkForPattern(rest, TP.For_Loop_Starting_Value_Definition_End): # then check for the end of the syntax
                    rest = rest[len(TP.For_Loop_Starting_Value_Definition_End):]
                    forLoop.startingValue = expression              # set &
                    return parseForLoop(rest, forLoop, nestLevel)   # continue
        #TODO: ADD ERROR HANDLING
        unknownError(__file__) # Some unexpected syntax
    elif forLoop.comparisonOperator == None: # If our for loop doesnt have a comparison operator yet, parse it!
        if isinstance(token, Tokens.Logic_Operator): # We, ofcourse, expect a logic/comparison operator.
            forLoop.comparisonOperator = token
            return parseForLoop(rest, forLoop, nestLevel)
        #TODO: ADD ERROR HANDLING
        unknownError(__file__) # Some unexpected syntax
    elif forLoop.body == None: # If our for loop doesnt have a body yet, parse it!
        if checkForPattern(tokens, TP.For_Loop_Body_Definition): # The body is just like any other code block, so we parse it.
            rest, codeBlock = parseCodeBlock(tokens[len(TP.For_Loop_Body_Definition):], ASTc.Code_Block(nestLevel + 1), nestLevel+1)
            if checkForPattern(rest, TP.For_Loop_Body_Definition_End): # Check for the body end syntax.
                forLoop.body = codeBlock                               # If it's there we can add our codeblock.
                return parseForLoop(rest[len(TP.For_Loop_Body_Definition_End):], forLoop, nestLevel)
        #TODO: ADD ERROR HANDLING
        print(rest[1])
        unknownError(__file__) # Some unexpected syntax
    elif forLoop.increment == None: # If our for loop doesnt have an incrementer yet, parse it!
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
        unknownError(__file__) # Some unexpected syntax
    elif forLoop.controlValue == None: # If our for loop doesnt have a control value yet, parse it!
        if isinstance(token, Tokens.Value) or isinstance(token, Tokens.Expression_Bracket_Open):
            rest, expression = parseExpression(tokens, ASTc.Expression(nestLevel + 1), nestLevel+1)
            if checkForPattern(rest, TP.For_Loop_End):
                forLoop.controlValue = expression
                return rest[len(TP.For_Loop_End):], forLoop
        #TODO: ADD ERROR HANDLING
        unknownError(__file__) # Some unexpected syntax
    #TODO: ADD ERROR HANDLING
    unknownError(__file__) # Some unexpected syntax

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

@timer
def parse(tokens : List[Tokens.Token]) -> List[ASTc.AST]:
    ASTs = parseNext(tokens, [], 1)
    # print(f"Constructed {len(ASTs)} ASTs.\n")
    # for ast in ASTs:
    #     print(ast)
    ASTs = squashASTList(ASTs)
    ASTs = checkForMissingImplementations(ASTs)
    return ASTs
