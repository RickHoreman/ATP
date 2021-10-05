from inspect import getargvalues, getclosurevars
import AST_classes as ASTc
from typing import List, Tuple, Union, TypeVar
import Tokens
import Token_Patterns as TP
from utilities import unknownError, find, stripHonorific

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

    def addVariable(self, identifier : Tokens.Identifier, value : Tokens.Value):
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
                # variable doesnt exist error
                #TODO: ADD ERROR HANDLING
                unknownError(__file__)
        else:
            # no scope error
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)

def initParameters(programState : Program_State, identifierList : ASTc.Parameter_List, valueList : ASTc.Parameter_List) -> Program_State:
    if len(identifierList.values) <= 0 or len(valueList.values) <= 0:
        return programState
    identifier = identifierList.pop()
    value = valueList.pop()
    programState.addVariable(identifier, value)
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
def solve(left : Tokens.Value, operator : Tokens.Operator, right : Tokens.Value) -> A:
    if isinstance(operator, Tokens.Addition):
        return left.value + right.value
    elif isinstance(operator, Tokens.Subtraction):
        return left.value - right.value
    elif isinstance(operator, Tokens.Greater_Than_Or_Equal):
        return left.value >= right.value
    elif isinstance(operator, Tokens.Smaller_Than_Or_Equal):
        return left.value <= right.value
    elif isinstance(operator, Tokens.Greater_Than):
        return left.value > right.value
    elif isinstance(operator, Tokens.Smaller_Than):
        return left.value < right.value

A = TypeVar('A')
def solveExpression(programState : Program_State, expression : Union[ASTc.Expression, Tokens.Integer, Tokens.Boolean]) -> A:
    if isinstance(expression, Tokens.Integer) or isinstance(expression, Tokens.Boolean):
        return expression.value
    elif isinstance(expression, ASTc.Function_Call):
        return runFunctionCall(programState, expression)
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

A = TypeVar('A')
def runCodeBlock(programState : Program_State, codeBlock : ASTc.Code_Block, progress : int=0) -> A:
    if progress >= len(codeBlock.code):
        return None
    code = codeBlock.code[progress]
    progress += 1
    if isinstance(code, ASTc.Variable_Assignment):
        programState.addVariable(code.identifier, solveExpression(programState, code.expression))
    if isinstance(code, ASTc.If_Statement):
        if programState.getValue(code.identifier) == solveExpression(programState, code.expression):
            result = runCodeBlock(programState, code.trueCodeBlock, 0)
            if result != None:
                return result
    # CONTINUE HERE
    return runCodeBlock(programState, codeBlock, progress)

A = TypeVar('A')
def runAST(programState : Program_State, ast : ASTc.AST, parameterList : ASTc.Parameter_List) -> A:
    if len(ast.parameterList.values) == len(parameterList.values):
        programState.addScope(ast.identifier)
        programState.currentScope = ast.identifier.name
        programState = initParameters(programState, ast.parameterList, parameterList)
        return runCodeBlock(programState, ast.codeBlock)
    else:
        # parameter mismatch error
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)

A = TypeVar('A')
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