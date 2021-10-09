from inspect import getargvalues, getclosurevars
import AST_classes as ASTc
from typing import List, Union, TypeVar
import Tokens
import Token_Patterns as TP
from utilities import unknownError, find, stripHonorific, timer
from copy import deepcopy

class Program_State():
    '''A datatype capable of containing scopes for (recursive!) function calls.'''
    def __init__(self, ASTs : List[ASTc.AST]):                          # The structure of the scope container is as follows:
        self.ASTs = ASTs                                                # A dictionary, the name of the scope/AST/function as the key,
        self.scopes = dict() # dict(str, List[dict(str, Tokens.Value)]) # and a list as value. This is like a little stack, every time
        self.currentScope = None                                        # we need a new scope with a name that already exists, we add
                                                                        # a new dictiory to this list, and remove it once we leave the scope.
    def addScope(self, identifier : Tokens.Identifier) -> None:         # This deepest dictionary simply contains variableName;value pairs.
        '''Operator for adding a new scope to the program state.'''
        if identifier.name not in self.scopes: # If no scope exists under that name yet,
            self.scopes[identifier.name] = [dict()] # add it with a list containing one dict as value.
        else:
            self.scopes[identifier.name].append(dict()) # Otherwise, add a new dict to the respective list.

    def popScope(self, identifier : Tokens.Identifier) -> None:
        '''Operator for popping a scope from the program state. Scope is not actually returned.'''
        if identifier.name in self.scopes:
            if len(self.scopes[identifier.name]) >= 1: # If there's multiple scopes under that name, only pop the front most.
                self.scopes[identifier.name].pop(len(self.scopes[identifier.name])-1)
            else:
                self.scopes.pop(identifier.name) # Otherwise remove the entire dictionary entry.

    def popCurrentScope(self) -> None:
        '''Operator for popping the current scope. Scope is not actually returned.'''
        self.popScope(self.currentScope)

    def setVariable(self, identifier : Tokens.Identifier, value : Tokens.Value):
        '''Operator for setting a variable in the program state. This can be a brand new variable or overwriting an existing one.'''
        if self.currentScope != None:
            self.scopes[self.currentScope][len(self.scopes[self.currentScope])-1][identifier.name] = value # Set the value in the front most scope under the currentScope's name.
        else:
            # no scope error
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)

    def getValue(self, identifier : Tokens.Identifier) -> Tokens.Value:
        '''Operator for getting the value of a variable. Throws error if the variable doesn't exist.'''
        if self.currentScope != None:
            if identifier.name in self.scopes[self.currentScope][len(self.scopes[self.currentScope])-1]:
                value = self.scopes[self.currentScope][len(self.scopes[self.currentScope])-1][identifier.name]
                if isinstance(value, Tokens.Identifier): # For explanation of the self.scopes' structure check the __init__ of Program_State.
                    return self.getValue(value) # If the value is another identifier, see if we can get it's value.
                else:
                    return value
            else:
                print(self.currentScope)
                print(identifier) # Just some, potentially, useful debug prints.
                print(self.scopes[self.currentScope][len(self.scopes[self.currentScope])-1])
                # variable doesnt exist error
                #TODO: ADD ERROR HANDLING
                unknownError(__file__)
        else:
            # no scope error
            #TODO: ADD ERROR HANDLING
            unknownError(__file__)

def initParameters(programState : Program_State, identifierList : ASTc.Parameter_List, valueList : ASTc.Parameter_List) -> Program_State:
    '''Initialises the entries in the identifier- and valueList as variables in the program state. Returns the new program state.'''
    if len(identifierList.values) <= 0 or len(valueList.values) <= 0:
        return programState
    identifier = identifierList.pop()
    value = valueList.pop()
    programState.setVariable(identifier, value)
    return initParameters(programState, identifierList, valueList)

A = TypeVar('A')
def runFunctionCall(programState : Program_State, functionCall : ASTc.Function_Call) -> A:
    '''Run the given function call using the program state. Returns the result of the function call.'''
    functionIndex = find(lambda ast, name: ast.identifier.name == name, programState.ASTs, functionCall.identifier.name)
    if functionIndex != None: # Find if the function exists in our AST list.
        return runAST(programState, programState.ASTs[functionIndex], functionCall.parameterList)
    else:
        # function doesnt exist error
        #TODO: ADD ERROR HANDLING
        unknownError(__file__)

A = TypeVar('A')
def solve(left : Union[Tokens.Value, int, bool], operator : Tokens.Operator, right : Union[Tokens.Value, int, bool]) -> A:
    '''Solves any "single-depth" expression. Returns the result of the expression.'''
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
    '''Solves any expression, including recursive expressions (expression in expression in expression...) and function calls. Returns the result of the expression.'''
    if isinstance(expression, Tokens.Identifier):                                           # It can occur than expression was already just
        return programState.getValue(expression)                                            # a single value during parsing. In these cases
    elif isinstance(expression, Tokens.Integer) or isinstance(expression, Tokens.Boolean):  # we just want to return the value.
        return expression.value
    elif isinstance(expression, ASTc.Function_Call):                                        # It can also be just a function call.
        return runFunctionCall(programState, expression)
    elif type(expression) == int or type(expression) == bool:
        return expression
    if isinstance(expression.left, ASTc.Expression):                # Solve any recursive expressions.
        expression.left = solveExpression(programState, expression) # (expression in expression in expression...)
    if isinstance(expression.right, ASTc.Expression):
        expression.right = solveExpression(programState, expression)
    if isinstance(expression.left, Tokens.Identifier):
        expression.left = programState.getValue(expression.left)    # Ask the program state for the values
    if isinstance(expression.right, Tokens.Identifier):             # of any identifiers.
        expression.right = programState.getValue(expression.right)
    if isinstance(expression.left, ASTc.Function_Call):                     # And run any function calls in
        expression.left = runFunctionCall(programState, expression.left)    # our left or right side.
    if isinstance(expression.right, ASTc.Function_Call):
        expression.right = runFunctionCall(programState, expression.right)
    # Left & right should now both be values.
    # However operator & right could still be None.
    if expression.operator == None and expression.right == None: # In this case the expression is just a single value on the left
        return expression.left                                   # so we simply return that.
    elif expression.left != None and expression.operator != None and expression.right != None: # If it's a full expression,
        if isinstance(expression.operator, Tokens.Operator):                                   # and our operator is actually an operator,
            return solve(expression.left, expression.operator, expression.right)               # solve (single-depth) the expression and return.
    # expression solving error
    #TODO: ADD ERROR HANDLING
    unknownError(__file__)

def solveParameterList(programState : Program_State, parameterList : ASTc.Parameter_List, solvedParameterList : ASTc.Parameter_List) -> ASTc.Parameter_List:
    '''This goes through all parameters in a function call's parameter list and solves any expressions it contains. Returns the "solved" parameter list.'''
    if len(parameterList.values) <= 0:
        return solvedParameterList
    parameter = parameterList.pop()
    solvedParameterList.append(solveExpression(programState, deepcopy(parameter)))
    return solveParameterList(programState, parameterList, solvedParameterList)

A = TypeVar('A')
def runForLoop(programState : Program_State, forLoop : ASTc.For_Loop) -> A:
    '''Runs a for loop and returns it's result, if any.'''
    if solve(programState.getValue(Tokens.Identifier(-1,-1, "Crabsさん")), forLoop.comparisonOperator, forLoop.controlValue):
        return None # Returns if our for-loops' condition has been met.
    else:
        result = runCodeBlock(programState, forLoop.body) # Otherwise run the code block once more.
        if result != None: # If the code block gave any return value,
            return result  # return that.
        programState.setVariable(Tokens.Identifier(-1,-1, "Crabsさん"), programState.getValue(Tokens.Identifier(-1,-1, "Crabsさん")) + forLoop.increment)
        return runForLoop(programState, forLoop) # Otherwise, increment our incrementer and loop again.

A = TypeVar('A')
def runCodeBlock(programState : Program_State, codeBlock : ASTc.Code_Block, progress : int=0) -> A:
    '''Runs a code block and returns its result, or None if we reach the end of the block.'''
    if progress >= len(codeBlock.code): # End of block reached.
        return None
    code = codeBlock.code[progress]
    progress += 1
    if isinstance(code, ASTc.Variable_Assignment):         # Deepcopies are used because the original expression was being changed, breaking loops :/, thanks python, very cool.
        programState.setVariable(code.identifier, solveExpression(programState, deepcopy(code.expression)))
    elif isinstance(code, ASTc.If_Statement):
        if programState.getValue(code.identifier) == solveExpression(programState, deepcopy(code.expression)):
            result = runCodeBlock(programState, code.trueCodeBlock, 0) # If the condition is true, run the true code block.
            if result != None:
                return result
        else:
            if code.elseCodeBlock != None: # If the condition is false and the else code block is defined, run it!
                result = runCodeBlock(programState, code.elseCodeBlock, 0)
                if result != None:
                    return result
    elif isinstance(code, ASTc.Return_Statement):
        return solveExpression(programState, deepcopy(code.expression))
    elif isinstance(code, ASTc.For_Loop): # The for-loop defines it's incrementer under the default name "Crabsさん" to make it accessible to the user during their loops.
        programState.setVariable(Tokens.Identifier(-1,-1, "Crabsさん"), solveExpression(programState, deepcopy(code.startingValue))) # Want this to be available to user!
        code.increment = solveExpression(programState, deepcopy(code.increment))        # Prep the input values
        code.controlValue = solveExpression(programState, deepcopy(code.controlValue))  # by solving any expressions first.
        result = runForLoop(programState, code) # Run it...
        if result != None:
            return result
    elif isinstance(code, ASTc.Print_Statement):
        print(solveExpression(programState, deepcopy(code.expression)))
    
    # CONTINUE HERE
    return runCodeBlock(programState, codeBlock, progress)

A = TypeVar('A')
def runAST(programState : Program_State, ast : ASTc.AST, parameterList : ASTc.Parameter_List) -> A:
    '''Runs any gives AST with gives parameter list. Returns the result of said AST.'''
    if len(ast.parameterList.values) == len(parameterList.values): # The number of parameters must match. We support no default values or anything (yet).
        parameterList = solveParameterList(programState, deepcopy(parameterList), ASTc.Parameter_List(parameterList.nestLevel)) # Reduce any expressions to single values.
        programState.addScope(ast.identifier)
        prevScope = programState.currentScope # We want to return to this scope afterwards.
        programState.currentScope = ast.identifier.name
        programState = initParameters(programState, deepcopy(ast.parameterList), deepcopy(parameterList))
        result = runCodeBlock(programState, ast.codeBlock)
        programState.currentScope = prevScope # Returns to previous scope.
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
    '''Runs the program (list of ASTs), starting with the function called sadge (can have any of the honorifics)(can be likened to main in c++). Returns the result of that function.'''
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