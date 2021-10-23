from io import TextIOWrapper
import AST_classes as ASTc
from typing import List, Union, TypeVar
import Tokens
import Token_Patterns as TP
from utilities import unknownCompilerError, find, stripHonorific, timer, romajifyHonorific
from copy import deepcopy

# addFunctionsToGlobalList :: TextIOWrapper -> [ASTc.AST] -> TextIOWrapper
def addFunctionsToGlobalList(outputFile : TextIOWrapper, ASTs : List[ASTc.AST]) -> TextIOWrapper:
    if len(ASTs) <= 0:
        return outputFile
    else:
        ast, *rest = ASTs
        outputFile.write(f"    .global {romajifyHonorific(ast.identifier.name)}\n")
        return addFunctionsToGlobalList(outputFile, rest)

# findVariables :: ASTc.Code_Block -> [Tokens.Identifier] -> Integer -> [Tokens.Identifier]
def findVariables(codeBlock : ASTc.Code_Block, variables : List[Tokens.Identifier], progress : int) -> List[Tokens.Identifier]:
    if progress >= len(codeBlock.code):
        return variables
    code = codeBlock.code[progress]
    progress += 1
    if isinstance(code, ASTc.Variable_Assignment):
        if find(lambda variable, identifier: variable.name == identifier.name, variables, code.identifier) == None:
            variables = variables + [code.identifier]
    elif isinstance(code, ASTc.If_Statement):
        variables = findVariables(code.trueCodeBlock, variables, 0)
        if code.elseCodeBlock != None:
            variables = findVariables(code.elseCodeBlock, variables, 0)
    elif isinstance(code, ASTc.For_Loop):
        if find(lambda variable, name: variable.name == name, variables, "Crabsさん") == None:
            variables = variables + [Tokens.Identifier(0, 0, "Crabsさん")]
        if find(lambda variable, name: variable.name == name, variables, "flControlValue") == None:
            variables = variables + [Tokens.Identifier(0, 0, "flControlValue")]
        if find(lambda variable, name: variable.name == name, variables, "flIncrement") == None:
            variables = variables + [Tokens.Identifier(0, 0, "flIncrement")]
        variables = findVariables(code.body, variables, 0)
    return findVariables(codeBlock, variables, progress)

# storeParametersOnStack :: TextIOWrapper -> Integer -> Integer -> TextIOWrapper
def storeParametersOnStack(outputFile : TextIOWrapper, nParameters : int, progress : int) -> TextIOWrapper:
    if nParameters <= 0:
        return outputFile
    else:
        outputFile.write(f"    str r{progress}, [r7, #{4*(progress+1)}]\n")
        return storeParametersOnStack(outputFile, nParameters-1, progress+1)

# storeParametersInRegisters :: TextIOWrapper -> [ASTc.Expression] -> Integer -> [Tokens.Identifier] -> TextIOWrapper
def storeParametersInRegisters(outputFile : TextIOWrapper, parameters : List[ASTc.Expression], progress : int, variables : List[Tokens.Identifier]) -> TextIOWrapper:
    if len(parameters) <= 0:
        return outputFile
    else:
        parameter, *rest = parameters
        outputFile = compileExpression(outputFile, parameter, progress, variables)
        return storeParametersInRegisters(outputFile, rest, progress+1, variables)

# compileFunctionCall :: TextIOWrapper -> ASTc.FunctionCall -> [Tokens.Identifier] -> TextIOWrapper
def compileFunctionCall(outputFile : TextIOWrapper, functionCall : ASTc.Function_Call, variables : List[Tokens.Identifier]) -> TextIOWrapper:
    outputFile = storeParametersInRegisters(outputFile, functionCall.parameterList.values, 0, variables)
    outputFile.write(f"    bl {romajifyHonorific(functionCall.identifier.name)}\n")
    return outputFile

# compileExpression :: TextIOWrapper -> ASTc.Expression -> Integer -> [Tokens.Identifier] -> TextIOWrapper
def compileExpression(outputFile : TextIOWrapper, expression : ASTc.Expression, resultAdress : int, variables : List[Tokens.Identifier]) -> TextIOWrapper:
    if isinstance(expression, Tokens.Identifier):
        outputFile.write(f"    ldr r{resultAdress}, [r7, #{(find(lambda variable, identifier: variable.name == identifier.name, variables, expression)+1)*4}]\n")
        return outputFile
    elif isinstance(expression, Tokens.Integer) or isinstance(expression, Tokens.Boolean):
        if expression.value >= 0:
            outputFile.write(f"    mov r{resultAdress}, #{int(expression.value)}\n")
        else:
            outputFile.write(f"    mov r{resultAdress}, #0\n")
            outputFile.write(f"    sub r{resultAdress}, r{resultAdress}, #{abs(expression.value)}\n")
        return outputFile
    elif isinstance(expression, ASTc.Function_Call):
        outputFile = compileFunctionCall(outputFile, expression, variables)
        outputFile.write(f"    mov r{resultAdress}, r0\n")
        return outputFile
    elif type(expression) == int or type(expression) == bool:
        if expression >= 0:
            outputFile.write(f"    mov r{resultAdress}, #{expression}\n")
        else:
            outputFile.write(f"    mov r{resultAdress}, #0\n")
            outputFile.write(f"    sub r{resultAdress}, r{resultAdress}, #{abs(expression)}\n")
        return outputFile
    if isinstance(expression.left, ASTc.Expression):
        outputFile = compileExpression(outputFile, expression.left, resultAdress, variables)
    if isinstance(expression.right, ASTc.Expression):
        outputFile.write(f"    push {'{'}r{resultAdress}{'}'}\n")
        outputFile = compileExpression(outputFile, expression.right, resultAdress, variables)
        outputFile.write(f"    mov r{resultAdress+1}, r{resultAdress}\n")
        outputFile.write(f"    pop {'{'}r{resultAdress}{'}'}\n")
    if isinstance(expression.left, Tokens.Identifier):
        outputFile.write(f"    ldr r{resultAdress}, [r7, #{(find(lambda variable, identifier: variable.name == identifier.name, variables, expression.left)+1)*4}]\n")
    if isinstance(expression.right, Tokens.Identifier):
        outputFile.write(f"    ldr r{resultAdress+1}, [r7, #{(find(lambda variable, identifier: variable.name == identifier.name, variables, expression.right)+1)*4}]\n")
    if isinstance(expression.left, ASTc.Function_Call):
        outputFile = compileFunctionCall(outputFile, expression.left, variables)
        outputFile.write(f"    mov r{resultAdress}, r0\n")
    if isinstance(expression.right, ASTc.Function_Call):
        outputFile = compileFunctionCall(outputFile, expression.right, variables)
        outputFile.write(f"    mov r{resultAdress+1}, r0\n")
    if isinstance(expression.left, Tokens.Integer) or isinstance(expression.left, Tokens.Boolean):
        outputFile.write(f"    mov r{resultAdress}, #{expression.left.value}\n")
    if isinstance(expression.right, Tokens.Integer) or isinstance(expression.right, Tokens.Boolean):
        outputFile.write(f"    mov r{resultAdress+1}, #{expression.right.value}\n")
    if expression.left != None and expression.operator != None and expression.right != None:
        if isinstance(expression.operator, Tokens.Addition):
            outputFile.write(f"    add r{resultAdress}, r{resultAdress}, r{resultAdress+1}\n")
        elif isinstance(expression.operator, Tokens.Subtraction):
            outputFile.write(f"    sub r{resultAdress}, r{resultAdress}, r{resultAdress+1}\n")
        elif isinstance(expression.operator, Tokens.Greater_Than_Or_Equal):
            outputFile.write(f"    cmp r{resultAdress}, r{resultAdress+1}\n")
            outputFile.write(f"    bge .ge{expression.operator.charNr}.{expression.operator.lineNr}true\n") # This should be a unique label
            outputFile.write(f"    mov r{resultAdress}, #0\n")
            outputFile.write(f"    b .ge{expression.operator.charNr}.{expression.operator.lineNr}end\n")
            outputFile.write(f".ge{expression.operator.charNr}.{expression.operator.lineNr}true:\n")
            outputFile.write(f"    mov r{resultAdress}, #1\n")
            outputFile.write(f".ge{expression.operator.charNr}.{expression.operator.lineNr}end:\n")
        elif isinstance(expression.operator, Tokens.Smaller_Than_Or_Equal):
            outputFile.write(f"    cmp r{resultAdress}, r{resultAdress+1}\n")
            outputFile.write(f"    ble .le{expression.operator.charNr}.{expression.operator.lineNr}true\n")
            outputFile.write(f"    mov r{resultAdress}, #0\n")
            outputFile.write(f"    b .le{expression.operator.charNr}.{expression.operator.lineNr}end\n")
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
    if progress >= len(codeBlock.code):
        return outputFile
    code = codeBlock.code[progress]
    progress += 1
    if isinstance(code, ASTc.Variable_Assignment):
        compileExpression(outputFile, code.expression, 1, variables)
        outputFile.write(f"    str r1, [r7, #{(find(lambda variable, identifier: variable.name == identifier.name, variables, code.identifier)+1)*4}]\n")
    elif isinstance(code, ASTc.If_Statement):
        outputFile.write(f"    ldr r1, [r7, #{(find(lambda variable, identifier: variable.name == identifier.name, variables, code.identifier)+1)*4}]\n")
        compileExpression(outputFile, code.expression, 2, variables)
        outputFile.write(f"    cmp r1, r2\n")
        if code.elseCodeBlock != None:
            outputFile.write(f"    bne .if{code.identifier.charNr}.{code.identifier.lineNr}else\n")
        else:
            outputFile.write(f"    bne .if{code.identifier.charNr}.{code.identifier.lineNr}end\n")
        compileCodeBlock(outputFile, code.trueCodeBlock, 0, variables)
        if code.elseCodeBlock != None:
            outputFile.write(f"    b .if{code.identifier.charNr}.{code.identifier.lineNr}end\n")
            outputFile.write(f".if{code.identifier.charNr}.{code.identifier.lineNr}else:\n")
            compileCodeBlock(outputFile, code.elseCodeBlock, 0, variables)
        outputFile.write(f".if{code.identifier.charNr}.{code.identifier.lineNr}end:\n")
    elif isinstance(code, ASTc.Return_Statement):
        compileExpression(outputFile, code.expression, 0, variables)
        outputFile.write(f"    add sp, sp, #{(len(variables) + 1) * 4}\n")
        outputFile.write("    pop {r7, pc}\n")
        return outputFile
    elif isinstance(code, ASTc.For_Loop):
        outputFile = compileExpression(outputFile, code.startingValue, 1, variables)
        outputFile.write(f"    str r1, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'Crabsさん')+1)*4}]\n")
        outputFile = compileExpression(outputFile, code.controlValue, 1, variables)
        outputFile.write(f"    str r1, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'flControlValue')+1)*4}]\n")
        outputFile = compileExpression(outputFile, code.increment, 1, variables)
        outputFile.write(f"    str r1, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'flIncrement')+1)*4}]\n")
        outputFile.write(f".fl{code.comparisonOperator.charNr}.{code.comparisonOperator.lineNr}:\n")
        outputFile = compileCodeBlock(outputFile, code.body, 0, variables)
        outputFile.write(f"    ldr r1, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'Crabsさん')+1)*4}]\n")
        outputFile.write(f"    ldr r2, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'flIncrement')+1)*4}]\n")
        outputFile.write(f"    add r1, r1, r2\n")
        outputFile.write(f"    str r1, [r7, #{(find(lambda variable, name: variable.name == name, variables, 'Crabsさん')+1)*4}]\n")
        outputFile = compileExpression(outputFile, ASTc.Expression(0, Tokens.Identifier(0, 0, "Crabsさん"), code.comparisonOperator, Tokens.Identifier(0, 0, "flControlValue")), 1, variables)
        outputFile.write(f"    cmp r1, #1\n")
        outputFile.write(f"    beq .fl{code.comparisonOperator.charNr}.{code.comparisonOperator.lineNr}\n")
    elif isinstance(code, ASTc.Function_Call):
        print("TODO5")
    return compileCodeBlock(outputFile, codeBlock, progress, variables)

# compileAST :: TextIOWrapper -> ASTc.AST -> TextIOWrapper
def compileAST(outputFile : TextIOWrapper, ast : ASTc.AST) -> TextIOWrapper:
    outputFile.write(f"\n{romajifyHonorific(ast.identifier.name)}:\n")
    variables = ast.parameterList.values
    variables = variables + findVariables(deepcopy(ast.codeBlock), [], 0)
    # for var in variables:
    #     print(var)
    outputFile.write("    push {r7, lr}\n")
    outputFile.write(f"    sub sp, sp, #{(len(variables) + 1) * 4}\n")
    outputFile.write("    mov r7, sp\n")
    outputFile = storeParametersOnStack(outputFile, len(ast.parameterList.values), 0)
    outputFile = compileCodeBlock(outputFile, ast.codeBlock, 0, variables)
    outputFile.write(f"    mov sp, r7\n")
    outputFile.write(f"    add sp, sp, #{(len(variables) + 1) * 4}\n")
    outputFile.write("    pop {r7, pc}\n")
    return outputFile

# run :: [ASTc.AST] -> None (outputs to file)
@timer
def compile(ASTs : List[ASTc.AST]):
    '''Compiles the program (list of ASTs). Will overwrite any files called Sadge.asm in the directory this is ran from.'''
    outputFile = open("../asm/Sadge.asm", 'w')
    outputFile.write("    .cpu cortex-m0\n")
    outputFile.write("    .text\n")
    outputFile.write("    .align 4\n")
    outputFile = addFunctionsToGlobalList(outputFile, deepcopy(ASTs))
    list(map(lambda ast: compileAST(outputFile, ast), ASTs))
    #outputFile.write("sadge_oujosama:\n    add r0, r0, #1\n    mov pc, lr")
    outputFile.close()