from io import TextIOWrapper
import AST_classes as ASTc
from typing import List, Union, TypeVar
import Tokens
import Token_Patterns as TP
from utilities import unknownCompilerError, find, stripHonorific, timer, romajifyHonorific
from copy import deepcopy

# addFunctionsToGlobalList :: TextIOWrapper -> [ASTc.AST] -> TextIOWrapper
def addFunctionsToGlobalList(outputFile : TextIOWrapper, ASTs : List[ASTc.AST]) -> TextIOWrapper:
    '''Adds all given ASTs to the globals labels as ".global functionName".'''
    if len(ASTs) <= 0:
        return outputFile
    else:
        ast, *rest = ASTs             # ASM & C++ dont like japanese characters so the honorifics need to be written in romaji :/
        outputFile.write(f"    .global {romajifyHonorific(ast.identifier.name)}\n")
        return addFunctionsToGlobalList(outputFile, rest)

# findVariables :: ASTc.Code_Block -> [Tokens.Identifier] -> Integer -> [Tokens.Identifier]
def findVariables(codeBlock : ASTc.Code_Block, variables : List[Tokens.Identifier], progress : int) -> List[Tokens.Identifier]:
    '''Finds all variables in a given code block and adds them to a big list, but only if no variable with the same name is already in there.'''
    if progress >= len(codeBlock.code):
        return variables
    code = codeBlock.code[progress]
    progress += 1
    if isinstance(code, ASTc.Variable_Assignment): # Making a new variable or changing it's value, so if it's not in the list yet, add it!
        if find(lambda variable, identifier: variable.name == identifier.name, variables, code.identifier) == None:
            variables = variables + [code.identifier]
    elif isinstance(code, ASTc.If_Statement): # If statements contain a code block or two, we want to add all the variables in there too!
        variables = findVariables(code.trueCodeBlock, variables, 0)
        if code.elseCodeBlock != None:
            variables = findVariables(code.elseCodeBlock, variables, 0)
    elif isinstance(code, ASTc.For_Loop): # For loops contain code blocks, and a few other "internal" variables.
        if find(lambda variable, name: variable.name == name, variables, "Crabsさん") == None: # This is the "iterator", using the さん honorific here means it's accessable to users.
            variables = variables + [Tokens.Identifier(0, 0, "Crabsさん")]
        if find(lambda variable, name: variable.name == name, variables, "flControlValue") == None: 
            variables = variables + [Tokens.Identifier(0, 0, "flControlValue")]                   # The controlvalue and increment however do not need to be accessable.
        if find(lambda variable, name: variable.name == name, variables, "flIncrement") == None:  # Instead we use values that can *never* overlap user defined variables.
            variables = variables + [Tokens.Identifier(0, 0, "flIncrement")]                      # (because users can only make variables with honorifics)
        variables = findVariables(code.body, variables, 0)
    return findVariables(codeBlock, variables, progress)

# storeParametersOnStack :: TextIOWrapper -> Integer -> Integer -> TextIOWrapper
def storeParametersOnStack(outputFile : TextIOWrapper, nParameters : int, progress : int) -> TextIOWrapper:
    '''Stores the values of register R0-R(nParameters) on stack. Used for right after a function call.'''
    if nParameters <= 0:
        return outputFile
    else:                                              # The function parameters will always be the first variables in a scope, so we can just use this progress rather than the list of found variables.
        outputFile.write(f"    str r{progress}, [r7, #{4*(progress+1)}]\n")
        return storeParametersOnStack(outputFile, nParameters-1, progress+1)

# storeParametersInRegisters :: TextIOWrapper -> [ASTc.Expression] -> Integer -> [Tokens.Identifier] -> TextIOWrapper
def storeParametersInRegisters(outputFile : TextIOWrapper, parameters : List[ASTc.Expression], progress : int, variables : List[Tokens.Identifier]) -> TextIOWrapper:
    '''Stores the values of function call parameters in the registers R0-R(len(parameters)), prepping them for the function call.'''
    if len(parameters) <= 0:
        return outputFile
    else:
        parameter, *rest = parameters
        outputFile = compileExpression(outputFile, parameter, progress, variables) # The parameter inputs are always expressions, so we can delegate most of the work.
        return storeParametersInRegisters(outputFile, rest, progress+1, variables)

# compileFunctionCall :: TextIOWrapper -> ASTc.FunctionCall -> [Tokens.Identifier] -> TextIOWrapper
def compileFunctionCall(outputFile : TextIOWrapper, functionCall : ASTc.Function_Call, variables : List[Tokens.Identifier]) -> TextIOWrapper:
    '''Prepares input values and then branches to the function.'''
    outputFile = storeParametersInRegisters(outputFile, functionCall.parameterList.values, 0, variables)
    outputFile.write(f"    bl {romajifyHonorific(functionCall.identifier.name)}\n")
    return outputFile

# compileExpression :: TextIOWrapper -> ASTc.Expression -> Integer -> [Tokens.Identifier] -> TextIOWrapper
def compileExpression(outputFile : TextIOWrapper, expression : ASTc.Expression, resultAdress : int, variables : List[Tokens.Identifier]) -> TextIOWrapper:
    '''Compiles the expression in such a way that the result ends up in R(resultAdress) and never uses more than two registers, namely R(resultAdress) and R(resultAdress+1).'''
    if isinstance(expression, Tokens.Identifier): # If the expression itself is an identifier, we just load it's value in R(resultAdress).
        outputFile.write(f"    ldr r{resultAdress}, [r7, #{(find(lambda variable, identifier: variable.name == identifier.name, variables, expression)+1)*4}]\n")
        return outputFile
    elif isinstance(expression, Tokens.Integer) or isinstance(expression, Tokens.Boolean): # Pretty much the same as with identifiers, except
        if expression.value >= 0:                                                          # if the value is negative, we cannot just do '#-1', for example.
            outputFile.write(f"    mov r{resultAdress}, #{int(expression.value)}\n")
        else:                                                                              # Instead we must put 0 in a register and subtract the value.
            outputFile.write(f"    mov r{resultAdress}, #0\n")
            outputFile.write(f"    sub r{resultAdress}, r{resultAdress}, #{abs(expression.value)}\n")
        return outputFile
    elif isinstance(expression, ASTc.Function_Call):                        # If it's a function call,
        outputFile = compileFunctionCall(outputFile, expression, variables) # delegate to compileFunctionCall
        outputFile.write(f"    mov r{resultAdress}, r0\n")                  # and then store the result in R(resultAdress)
        return outputFile
    elif type(expression) == int or type(expression) == bool: # Same thing as with token equivalents.
        if expression >= 0:
            outputFile.write(f"    mov r{resultAdress}, #{expression}\n")
        else:
            outputFile.write(f"    mov r{resultAdress}, #0\n")
            outputFile.write(f"    sub r{resultAdress}, r{resultAdress}, #{abs(expression)}\n")
        return outputFile
    if isinstance(expression.left, ASTc.Expression): # If the left side is another expression, just compile that, we don't have to worry about it overwriting R(resultAdress) or R(resultAdress+1).
        outputFile = compileExpression(outputFile, expression.left, resultAdress, variables)
    if isinstance(expression.right, ASTc.Expression): # If the right side is another expression, this means we want to first preserve the value in R(resultAdress), so we push that to stack first.
        outputFile.write(f"    push {'{'}r{resultAdress}{'}'}\n")                               # We could instead just pass resultAdress+1 to compileExpression, but this means if we have a lot of recursive expressions it can go out of bounds.
        outputFile = compileExpression(outputFile, expression.right, resultAdress, variables)
        outputFile.write(f"    mov r{resultAdress+1}, r{resultAdress}\n") # The result of the right side expression is now in R(resultAdress), but we want it in R(resultAdress+1)
        outputFile.write(f"    pop {'{'}r{resultAdress}{'}'}\n") # Pop R(resultAdress) again.
    if isinstance(expression.left, Tokens.Identifier): # An identifier? Just load it's value!
        outputFile.write(f"    ldr r{resultAdress}, [r7, #{(find(lambda variable, identifier: variable.name == identifier.name, variables, expression.left)+1)*4}]\n")
    if isinstance(expression.right, Tokens.Identifier): # An identifier? Just load it's value! (this time into R(resultAdress+1) because it's the right side)
        outputFile.write(f"    ldr r{resultAdress+1}, [r7, #{(find(lambda variable, identifier: variable.name == identifier.name, variables, expression.right)+1)*4}]\n")
    if isinstance(expression.left, ASTc.Function_Call):                             # If the left side is a function call,
        outputFile = compileFunctionCall(outputFile, expression.left, variables)    # delegate to compileFunctionCall,
        outputFile.write(f"    mov r{resultAdress}, r0\n")                          # and then store the result in R(resultAdress).
    if isinstance(expression.right, ASTc.Function_Call):                            # If the right side is a function call,
        outputFile = compileFunctionCall(outputFile, expression.right, variables)   # delegate to compileFunctionCall,
        outputFile.write(f"    mov r{resultAdress+1}, r0\n")                        # and then store the result in R(resultAdress+1).
    if isinstance(expression.left, Tokens.Integer) or isinstance(expression.left, Tokens.Boolean):
        if expression.left.value >= 0:                                                     # Same as with if the expression itself is an int or a bool.  
            outputFile.write(f"    mov r{resultAdress}, #{int(expression.left.value)}\n")  # If the value is negative, we cannot just do '#-1', for example.
        else:                                                                              # Instead we must put 0 in a register and subtract the value.
            outputFile.write(f"    mov r{resultAdress}, #0\n")
            outputFile.write(f"    sub r{resultAdress}, r{resultAdress}, #{abs(expression.left.value)}\n")
    if isinstance(expression.right, Tokens.Integer) or isinstance(expression.right, Tokens.Boolean):
        if expression.right.value >= 0:                                                      # Same as with if the expression itself is an int or a bool.  
            outputFile.write(f"    mov r{resultAdress+1}, #{int(expression.right.value)}\n") # If the value is negative, we cannot just do '#-1', for example.
        else:                                                                                # Instead we must put 0 in a register and subtract the value.
            outputFile.write(f"    mov r{resultAdress+1}, #0\n")
            outputFile.write(f"    sub r{resultAdress+1}, r{resultAdress+1}, #{abs(expression.right.value)}\n")
    if expression.left != None and expression.operator != None and expression.right != None: # This means we have a full expression with all fields filled.
        if isinstance(expression.operator, Tokens.Addition): # Addition is simple.
            outputFile.write(f"    add r{resultAdress}, r{resultAdress}, r{resultAdress+1}\n")
        elif isinstance(expression.operator, Tokens.Subtraction): # Same with subtraction.
            outputFile.write(f"    sub r{resultAdress}, r{resultAdress}, r{resultAdress+1}\n")
        elif isinstance(expression.operator, Tokens.Greater_Than_Or_Equal): # But the logic operator require a bit more (because I don't want to use more than two registers).
            outputFile.write(f"    cmp r{resultAdress}, r{resultAdress+1}\n")                               # First we compare, to set the flags and all that.
            outputFile.write(f"    bge .ge{expression.operator.charNr}.{expression.operator.lineNr}true\n") # Then we have our operator dependant branch statement. The branch happens when the operator would result in 'true'.
            outputFile.write(f"    mov r{resultAdress}, #0\n")                                              # Otherwise, put a 0 (false) in the result.
            outputFile.write(f"    b .ge{expression.operator.charNr}.{expression.operator.lineNr}end\n")    # And branch to the end of the operation.
            outputFile.write(f".ge{expression.operator.charNr}.{expression.operator.lineNr}true:\n")        # If the operator is true;
            outputFile.write(f"    mov r{resultAdress}, #1\n")                                              # Place a 1 (true) in the result.
            outputFile.write(f".ge{expression.operator.charNr}.{expression.operator.lineNr}end:\n")         # And we're done! All of the following operators work the same, just with different branch types.
        elif isinstance(expression.operator, Tokens.Smaller_Than_Or_Equal):
            outputFile.write(f"    cmp r{resultAdress}, r{resultAdress+1}\n")
            outputFile.write(f"    ble .le{expression.operator.charNr}.{expression.operator.lineNr}true\n") # The used labels are based off the type of branching we do, followed by the unique combination char nr and line nr of the operator.
            outputFile.write(f"    mov r{resultAdress}, #0\n")                                              # This way we can never end up with duplicate labels. (that would be bad).
            outputFile.write(f"    b .le{expression.operator.charNr}.{expression.operator.lineNr}end\n")    # This same label format is also used elsewhere, for example for if statements and for-loops.
            outputFile.write(f".le{expression.operator.charNr}.{expression.operator.lineNr}true:\n")
            outputFile.write(f"    mov r{resultAdress}, #1\n")
            outputFile.write(f".le{expression.operator.charNr}.{expression.operator.lineNr}end:\n")
        elif isinstance(expression.operator, Tokens.Greater_Than):
            outputFile.write(f"    cmp r{resultAdress}, r{resultAdress+1}\n")
            outputFile.write(f"    bgt .gt{expression.operator.charNr}.{expression.operator.lineNr}true\n")
            outputFile.write(f"    mov r{resultAdress}, #0\n")
            outputFile.write(f"    b .gt{expression.operator.charNr}.{expression.operator.lineNr}end\n")
            outputFile.write(f".gt{expression.operator.charNr}.{expression.operator.lineNr}true:\n")
            outputFile.write(f"    mov r{resultAdress}, #1\n")
            outputFile.write(f".gt{expression.operator.charNr}.{expression.operator.lineNr}end:\n")
        elif isinstance(expression.operator, Tokens.Smaller_Than):
            outputFile.write(f"    cmp r{resultAdress}, r{resultAdress+1}\n")
            outputFile.write(f"    blt .lt{expression.operator.charNr}.{expression.operator.lineNr}true\n")
            outputFile.write(f"    mov r{resultAdress}, #0\n")
            outputFile.write(f"    b .lt{expression.operator.charNr}.{expression.operator.lineNr}end\n")
            outputFile.write(f".lt{expression.operator.charNr}.{expression.operator.lineNr}true:\n")
            outputFile.write(f"    mov r{resultAdress}, #1\n")
            outputFile.write(f".lt{expression.operator.charNr}.{expression.operator.lineNr}end:\n")
    return outputFile

# compileCodeBlock :: TextIOWrapper -> ASTc.Code_Block -> Integer -> [Tokens.Identifier] -> TextIOWrapper
def compileCodeBlock(outputFile : TextIOWrapper, codeBlock : ASTc.Code_Block, progress : int, variables : List[Tokens.Identifier]) -> TextIOWrapper:
    '''Goes through the code block checking for all possible contents and compiling each in their specific way.'''
    if progress >= len(codeBlock.code):
        return outputFile
    code = codeBlock.code[progress]
    progress += 1
    if isinstance(code, ASTc.Variable_Assignment): # For assignments we just want to compile the expression and then save the result of that to the variable's stack adress.
        outputFile = compileExpression(outputFile, code.expression, 1, variables)
        outputFile.write(f"    str r1, [r7, #{(find(lambda variable, identifier: variable.name == identifier.name, variables, code.identifier)+1)*4}]\n")
    elif isinstance(code, ASTc.If_Statement): # We first store the value of the identifier on the left side of the if statement in R1 \/
        outputFile.write(f"    ldr r1, [r7, #{(find(lambda variable, identifier: variable.name == identifier.name, variables, code.identifier)+1)*4}]\n")
        outputFile = compileExpression(outputFile, code.expression, 2, variables) # We then get the result of the expression in R2
        outputFile.write(f"    cmp r1, r2\n") # Then we compare those.
        if code.elseCodeBlock != None: # If the if statement is false we want to either jump to the end or the else code block, depending on wether the else code block exists or not.
            outputFile.write(f"    bne .if{code.identifier.charNr}.{code.identifier.lineNr}else\n") # Jump to else code block.
        else:
            outputFile.write(f"    bne .if{code.identifier.charNr}.{code.identifier.lineNr}end\n") # Jump to end
        outputFile = compileCodeBlock(outputFile, code.trueCodeBlock, 0, variables) # If the if statement is true, we want to execute the true code block, this always exists.
        if code.elseCodeBlock != None:                                                           # If the else block is defined,
            outputFile.write(f"    b .if{code.identifier.charNr}.{code.identifier.lineNr}end\n") # we want to jump to the end of the if statement at the end of the true block.
            outputFile.write(f".if{code.identifier.charNr}.{code.identifier.lineNr}else:\n")     # And define the label for the else block.
            compileCodeBlock(outputFile, code.elseCodeBlock, 0, variables)                       # And ofcourse compile the else block.
        outputFile.write(f".if{code.identifier.charNr}.{code.identifier.lineNr}end:\n") # We always need the end label at the end of the if statement.
    elif isinstance(code, ASTc.Return_Statement): # A return statement just has an expression.
        outputFile = compileExpression(outputFile, code.expression, 0, variables) # Just get the expression to evaluate right into R0, that way we dont have to move it after.
        outputFile.write(f"    mov sp, r7\n")
        outputFile.write(f"    add sp, sp, #{(len(variables) + 1) * 4}\n") # Give back our reserved space on the stack. 
        outputFile.write("    pop {r7, pc}\n") # And pop the pc (and R7)
        return outputFile # No need to compile this code block any further.
    elif isinstance(code, ASTc.For_Loop): # For loops are... nice...
        outputFile = compileExpression(outputFile, code.startingValue, 1, variables) # The starting value, control value, and increment can all be expressions, so compile them.
        outputFile.write(f"    str r1, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'Crabsさん')+1)*4}]\n") # And then place them in their respective variables.
        outputFile = compileExpression(outputFile, code.controlValue, 1, variables)                                                  # The incrementor (not increment value!) is stored using an honorific so that is actually accessable to users.
        outputFile.write(f"    str r1, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'flControlValue')+1)*4}]\n") # The other two don't have honorifics because users dont need to interact with them,
        outputFile = compileExpression(outputFile, code.increment, 1, variables)                                                          # and we'd rather use values that can't overlap user defined variables
        outputFile.write(f"    str r1, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'flIncrement')+1)*4}]\n")    # (seeing as they can only define variables with honorifics.)
        outputFile.write(f".fl{code.comparisonOperator.charNr}.{code.comparisonOperator.lineNr}:\n") # Place the label for the start of the loop.
        outputFile = compileCodeBlock(outputFile, code.body, 0, variables)                           # then compile the loop body.
        outputFile.write(f"    ldr r1, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'Crabsさん')+1)*4}]\n")    # Get the values of our incrementer
        outputFile.write(f"    ldr r2, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'flIncrement')+1)*4}]\n")  # and increment value.
        outputFile.write(f"    add r1, r1, r2\n")                                                                                       # Add them togethe (increment the incrementer with the increment value)
        outputFile.write(f"    str r1, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'Crabsさん')+1)*4}]\n")    # store the result.
        outputFile = compileExpression(outputFile, ASTc.Expression(0, Tokens.Identifier(0, 0, "Crabsさん"), code.comparisonOperator, Tokens.Identifier(0, 0, "flControlValue")), 1, variables) # Do the control comparison (check whether the loop is over or not)
        outputFile.write(f"    cmp r1, #1\n") # Check if the above expression evaluated to true
        outputFile.write(f"    beq .fl{code.comparisonOperator.charNr}.{code.comparisonOperator.lineNr}\n") # If so, continue the loop, otherwise, we're done here :)
    elif isinstance(code, ASTc.Print_Statement):                                  # Printing uses a C defined print function!
        outputFile = compileExpression(outputFile, code.expression, 0, variables) # Compile the to-be-printed-expression (with the result going into R0)
        outputFile.write(f"    bl print\n")                                       # call the C defined print function.
    elif isinstance(code, ASTc.Function_Call): # Just delegate to compileFunctionCall
        outputFile = compileFunctionCall(outputFile, code, variables)   # I am aware that nothing is being done with the potential return value of the function
    return compileCodeBlock(outputFile, codeBlock, progress, variables) # but this doesnt need to happen, this is a sole function call, the result of which is not being placed in any variable.
            # ^Compile the next line in the codeblock.

# compileAST :: TextIOWrapper -> ASTc.AST -> TextIOWrapper
def compileAST(outputFile : TextIOWrapper, ast : ASTc.AST) -> TextIOWrapper:
    '''Compiles the entire given AST into the given outputFile.'''
    outputFile.write(f"\n{romajifyHonorific(ast.identifier.name)}:\n") # Make the (romajified) label for the function.
    variables = ast.parameterList.values # Set the function's parameters to be the first variables in our variable list.
    variables = variables + findVariables(deepcopy(ast.codeBlock), [], 0) # Then find all the other variables in the function and add them to the list.
    outputFile.write("    push {r7, lr}\n") # We are going to use R7 and potentially call another function, so push R7 and the link register onto the stack.
    outputFile.write(f"    sub sp, sp, #{(len(variables) + 1) * 4}\n") # Then reserve enough stack space for all our variables.
    outputFile.write("    mov r7, sp\n") # And save the start of that memory segment to R7 (in case we do more pushing & popping).
    outputFile = storeParametersOnStack(outputFile, len(ast.parameterList.values), 0) # Then get the input values of the function parameters and store them in there respective stack adresses.
    outputFile = compileCodeBlock(outputFile, ast.codeBlock, 0, variables) # Then compile the function's code block.
    outputFile.write(f"    mov sp, r7\n")                              # End by giving back the
    outputFile.write(f"    add sp, sp, #{(len(variables) + 1) * 4}\n") # reserved stack space.
    outputFile.write("    pop {r7, pc}\n")                             # And popping the program counter (and R7)
    return outputFile

# run :: [ASTc.AST] -> None (outputs to file)
@timer
def compile(ASTs : List[ASTc.AST]):
    '''Compiles the program (list of ASTs). Will overwrite any files called Sadge.asm in the directory this is ran from.'''
    outputFile = open("../asm/Sadge.asm", 'w')
    outputFile.write("    .cpu cortex-m0\n") # Put all the base information about the .asm file.
    outputFile.write("    .text\n")
    outputFile.write("    .align 4\n")
    outputFile = addFunctionsToGlobalList(outputFile, deepcopy(ASTs)) # Then add all function labels to .global
    list(map(lambda ast: compileAST(outputFile, ast), ASTs))          # And compile all the functions!
    outputFile.close()