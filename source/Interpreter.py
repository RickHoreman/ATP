from inspect import getargvalues, getclosurevars
import AST_classes as ASTc
from typing import List, Union, TypeVar
import Tokens
import Token_Patterns as TP
from utilities import unknownError, find, stripHonorific, timer
from copy import deepcopy

class Program_State():
    def __init__(self, ASTs : List[ASTc.AST]):
        self.ASTs = ASTs
        self.scopes = dict() # dict(str, List[dict(str, Tokens.Value)])
        self.currentScope = None
    
    def addScope(self, identifier : Tokens.Identifier) -> None:
        if identifier not in self.scopes:
            self.scopes[identifier.name] = [dict()]
        else:
            self.scopes[identifier.name].append(dict())

    def popScope(self, identifier : Tokens.Identifier) -> None:
        if identifier in self.scopes:
            if len(self.scopes[identifier.name]) >= 1:
                self.scopes[identifier.name].pop(len(self.scopes[identifier.name])-1)
            else:
                self.scopes.pop(identifier.name)

    def popCurrentScope(self) -> None:
        self.popScope(self.currentScope)

    def setVariable(self, identifier : Tokens.Identifier, value : Tokens.Value):
        if self.currentScope != None:
            self.scopes[self.currentScope][len(self.scopes[self.currentScope])-1][identifier.name] = value
        else:
            # no scope error
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)

    def getValue(self, identifier : Tokens.Identifier) -> Tokens.Value:
        if self.currentScope != None:
            if identifier.name in self.scopes[self.currentScope][len(self.scopes[self.currentScope])-1]:
                value = self.scopes[self.currentScope][len(self.scopes[self.currentScope])-1][identifier.name]
                if isinstance(value, Tokens.Identifier):
                    return self.getValue(value)
                else:
                    return value
            else:
                print(self.currentScope)
                print(identifier)
                print(self.scopes[self.currentScope][len(self.scopes[self.currentScope])-1])
                # variable doesnt exist error
                #TODO: ADD ERROR HANDLING
                unknownError(__file__)
        else:
            # no scope error
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)

    def printCurrentScope(self): #Debug voor tijdens maken dus gebruikt voor gemak even een loop
        if self.currentScope != None:
            for variable, value in self.scopes[self.currentScope][len(self.scopes[self.currentScope])-1].items():
                print(f"{variable}: {value}")

def initParameters(programState : Program_State, identifierList : ASTc.Parameter_List, valueList : ASTc.Parameter_List) -> Program_State:
    if len(identifierList.values) <= 0 or len(valueList.values) <= 0:
        return programState
    identifier = identifierList.pop()
    value = valueList.pop()
    programState.setVariable(identifier, value)
    return initParameters(programState, identifierList, valueList)

A = TypeVar('A')
def runFunctionCall(programState : Program_State, functionCall : ASTc.Function_Call) -> A:
    functionIndex = find(lambda ast, name: ast.identifier.name == name, programState.ASTs, functionCall.identifier.name)
    if functionIndex != None:
        return runAST(programState, programState.ASTs[functionIndex], functionCall.parameterList)
    else:
        # function doesnt exist error
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)

A = TypeVar('A')
def solve(left : Union[Tokens.Value, int, bool], operator : Tokens.Operator, right : Union[Tokens.Value, int, bool]) -> A:
    if isinstance(left, Tokens.Value):
        left = left.value
    if isinstance(right, Tokens.Value):
        right = right.value
    if isinstance(operator, Tokens.Addition):
        return left + right
    elif isinstance(operator, Tokens.Subtraction):
        return left - right
    elif isinstance(operator, Tokens.Greater_Than_Or_Equal):
        return left >= right
    elif isinstance(operator, Tokens.Smaller_Than_Or_Equal):
        return left <= right
    elif isinstance(operator, Tokens.Greater_Than):
        return left > right
    elif isinstance(operator, Tokens.Smaller_Than):
        return left < right

A = TypeVar('A')
def solveExpression(programState : Program_State, expression : Union[ASTc.Expression, Tokens.Integer, Tokens.Boolean]) -> A:
    if isinstance(expression, Tokens.Identifier):
        return programState.getValue(expression)
    elif isinstance(expression, Tokens.Integer) or isinstance(expression, Tokens.Boolean):
        return expression.value
    elif isinstance(expression, ASTc.Function_Call):
        return runFunctionCall(programState, expression)
    elif type(expression) == int or type(expression) == bool:
        return expression
    if isinstance(expression.left, ASTc.Expression):
        expression.left = solveExpression(programState, expression)
    if isinstance(expression.right, ASTc.Expression):
        expression.right = solveExpression(programState, expression)
    if isinstance(expression.left, Tokens.Identifier):
        expression.left = programState.getValue(expression.left)
    if isinstance(expression.right, Tokens.Identifier):
        expression.right = programState.getValue(expression.right)
    if isinstance(expression.left, ASTc.Function_Call):
        expression.left = runFunctionCall(programState, expression.left)
    if isinstance(expression.right, ASTc.Function_Call):
        expression.right = runFunctionCall(programState, expression.right)
    # Left & right should now both be values
    # However operator & right could still be None
    if expression.operator == None and expression.right == None:
        return expression.left
    elif expression.left != None and expression.operator != None and expression.right != None:
        if isinstance(expression.operator, Tokens.Operator):
            return solve(expression.left, expression.operator, expression.right)
    # expression solving error
    #TODO: ADD ERROR HANDLING
    unknownError(__file__)

def solveParameterList(programState : Program_State, parameterList : ASTc.Parameter_List, solvedParameterList : ASTc.Parameter_List) -> ASTc.Parameter_List:
    if len(parameterList.values) <= 0:
        return solvedParameterList
    parameter = parameterList.pop()
    solvedParameterList.append(solveExpression(programState, deepcopy(parameter)))
    return solveParameterList(programState, parameterList, solvedParameterList)

A = TypeVar('A')
def runForLoop(programState : Program_State, forLoop : ASTc.For_Loop) -> A:
    if solve(programState.getValue(Tokens.Identifier(-1,-1, "Crabsさん")), forLoop.comparisonOperator, forLoop.controlValue):
        return None
    else:
        # programState.printCurrentScope()
        result = runCodeBlock(programState, forLoop.body)
        if result != None:
            return result
        # print("pogu")
        # programState.printCurrentScope()
        programState.setVariable(Tokens.Identifier(-1,-1, "Crabsさん"), programState.getValue(Tokens.Identifier(-1,-1, "Crabsさん")) + forLoop.increment)
        #print(programState.getValue(Tokens.Identifier(-1,-1, "result殿")))
        return runForLoop(programState, forLoop)

A = TypeVar('A')
def runCodeBlock(programState : Program_State, codeBlock : ASTc.Code_Block, progress : int=0) -> A:
    if progress >= len(codeBlock.code):
        return None
    code = codeBlock.code[progress]
    progress += 1
    if isinstance(code, ASTc.Variable_Assignment):
        programState.setVariable(code.identifier, solveExpression(programState, deepcopy(code.expression)))
    elif isinstance(code, ASTc.If_Statement):
        if programState.getValue(code.identifier) == solveExpression(programState, deepcopy(code.expression)):
            result = runCodeBlock(programState, code.trueCodeBlock, 0)
            if result != None:
                return result
        else:
            if code.elseCodeBlock != None:
                result = runCodeBlock(programState, code.elseCodeBlock, 0)
                if result != None:
                    return result
    elif isinstance(code, ASTc.Return_Statement):
        return solveExpression(programState, deepcopy(code.expression))
    elif isinstance(code, ASTc.For_Loop):
        programState.setVariable(Tokens.Identifier(-1,-1, "Crabsさん"), solveExpression(programState, deepcopy(code.startingValue))) # Want this to be available to user!
        code.increment = solveExpression(programState, deepcopy(code.increment))
        code.controlValue = solveExpression(programState, deepcopy(code.controlValue))
        result = runForLoop(programState, code)
        if result != None:
                return result
    elif isinstance(code, ASTc.Print_Statement):
        print(solveExpression(programState, deepcopy(code.expression)))
    
    # CONTINUE HERE
    return runCodeBlock(programState, codeBlock, progress)

A = TypeVar('A')
def runAST(programState : Program_State, ast : ASTc.AST, parameterList : ASTc.Parameter_List) -> A:
    if len(ast.parameterList.values) == len(parameterList.values):
        parameterList = solveParameterList(programState, deepcopy(parameterList), ASTc.Parameter_List(parameterList.nestLevel))
        programState.addScope(ast.identifier)
        prevScope = programState.currentScope
        programState.currentScope = ast.identifier.name
        programState = initParameters(programState, deepcopy(ast.parameterList), deepcopy(parameterList))
        result = runCodeBlock(programState, ast.codeBlock)
        # if ast.identifier.name == "sommigさま":
        #     programState.printCurrentScope()
        programState.currentScope = prevScope
        return result
    else:
        print(ast)
        print(parameterList)
        # parameter mismatch error
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)

A = TypeVar('A')
@timer
def run(ASTs : List[ASTc.AST], arguments : List) -> A:
    programState = Program_State(ASTs)
    sadgeIndex = find(lambda ast, name: stripHonorific(ast.identifier.name) == name, ASTs, "sadge")
    if sadgeIndex == None:
        # missing main function error
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)
    else:
        parameterList = ASTc.Parameter_List(0)
        parameterList.values = arguments
        return runAST(programState, ASTs[sadgeIndex], parameterList)