import Tokens
from typing import Union

class SimpleStatement:
    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}."
    
class Assignment(SimpleStatement):
    def __init__(self, variableName : Tokens.Identifier, value) -> None:
        self.variableName = variableName
        self.value = value

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}. Variable name: {self.variableName}, value: {self.value}"

class Expression_Base():
    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}."

class Expression(Expression_Base):
    # __init__ :: Union[Expression_Base, Tokens.Value] -> Tokens.Operator -> Union[Expression_Base, Tokens.Value] -> None
    def __init__(self, left : Union[Expression_Base, Tokens.Value]=None, operator : Tokens.Operator=None, right : Union[Expression_Base, Tokens.Value]=None) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}.\n{str(self.left)}\n{str(self.operator)}\n{str(self.right)}"

class Code_Block(SimpleStatement):
    def __init__(self) -> None:
        self.code = []

    def append(self, statement : SimpleStatement):
        self.code.append(statement)

    # __str__ :: None -> String
    def __str__(self) -> str:
        nstr = ""#repeatStr("   ", self.nestlevel) #ADD NEST LEVEL
        statestr = ''.join(map(lambda st: nstr + str(st) + "\n", self.code))
        return f"{self.__class__.__name__}.\n" + statestr

class Parameter_List():
    def __init__(self) -> None:
        self.identifiers = []

    def append(self, identifier : Tokens.Identifier):
        self.identifiers.append(identifier)

    # __str__ :: None -> String
    def __str__(self) -> str:
        nstr = ""#repeatStr("   ", self.nestlevel) #ADD NEST LEVEL
        statestr = ''.join(map(lambda st: nstr + "\n" + str(st), self.identifiers))
        return f"{self.__class__.__name__}." + statestr

class If_Statement(SimpleStatement):
    def __init__(self, identifier : Tokens.Identifier=None, expression : Expression=None, trueCodeBlock : Code_Block=None, elseCodeBlock : Code_Block=None):
        self.identifier = identifier
        self.expression = expression
        self.trueCodeBlock = trueCodeBlock
        self.elseCodeBlock = elseCodeBlock

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}.\n{str(self.identifier)}\n{str(self.expression)}\n{str(self.trueCodeBlock)}\n{str(self.elseCodeBlock)}"

class Variable_Assignment(SimpleStatement):
    def __init__(self, identifier : Tokens.Identifier=None, expression : Expression=None):
        self.identifier = identifier
        self.expression = expression

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}.\n{str(self.identifier)}\n{str(self.expression)}"

class Function_Call():
    def __init__(self, identifier : Tokens.Identifier=None, parameterList : Parameter_List=None) -> None:
        self.identifier = identifier
        self.parameterList = parameterList
        
    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}.\n{self.identifier}.\n{str(self.parameterList)}"

class Return_Statement(SimpleStatement):
    def __init__(self, expression : Union[Expression, Function_Call]=None):
        self.expression = expression

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}.\n{str(self.expression)}"

class For_Loop():
    def __init__(self, startingValue : Union[Expression, int]=None, comparisonOperator : Tokens.Logic_Operator=None, body : Code_Block=None, increment : Union[Expression, int]=None, controlValue : Expression=None) -> None:
        self.startingValue = startingValue
        self.comparisonOperator = comparisonOperator
        self.body = body
        self.increment = increment
        self.controlValue = controlValue
        
    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}.\n{self.startingValue}\n{self.comparisonOperator}.\n{str(self.body)}\n{str(self.increment)}\n{str(self.controlValue)}"

class AST():
    def __init__(self, identifier : Tokens.Identifier=None, parameterList : Parameter_List=None, codeBlock : Code_Block=None) -> None:
        self.identifier = identifier
        self.parameterList = parameterList
        self.codeBlock = codeBlock
        
    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}.\n{self.identifier}.\n{str(self.parameterList)}\n{str(self.codeBlock)}"
