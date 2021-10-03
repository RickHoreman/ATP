import Tokens
from typing import Union
from utilities import space

class SimpleStatement:
    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

class Expression_Base():
    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

class Expression(Expression_Base):
    # __init__ :: Int -> Union[Expression_Base, Tokens.Value] -> Tokens.Operator -> Union[Expression_Base, Tokens.Value] -> None
    def __init__(self, nestLevel : int, left : Union[Expression_Base, Tokens.Value]=None, operator : Tokens.Operator=None, right : Union[Expression_Base, Tokens.Value]=None) -> None:
        self.nestLevel = nestLevel
        self.left = left
        self.operator = operator
        self.right = right

    # __str__ :: None -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Left: {str(self.left)}\n{spacing}Operator: {str(self.operator)}\n{spacing}Right: {str(self.right)}"

class Code_Block(SimpleStatement):
    def __init__(self, nestLevel : int) -> None:
        self.nestLevel = nestLevel
        self.code = []

    def append(self, statement : SimpleStatement):
        self.code.append(statement)

    # __str__ :: None -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        statestr = ''.join(map(lambda st: "\n" + spacing + str(st), self.code))
        return f"{self.__class__.__name__}" + statestr

class Parameter_List():
    def __init__(self, nestLevel : int) -> None:
        self.nestLevel = nestLevel
        self.identifiers = []

    def append(self, identifier : Tokens.Identifier):
        self.identifiers.append(identifier)

    # __str__ :: None -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        statestr = ''.join(map(lambda st: "\n" + spacing + str(st), self.identifiers))
        return f"{self.__class__.__name__}" + statestr

class If_Statement(SimpleStatement):
    def __init__(self, nestLevel : int, identifier : Tokens.Identifier=None, expression : Expression=None, trueCodeBlock : Code_Block=None, elseCodeBlock : Code_Block=None):
        self.nestLevel = nestLevel
        self.identifier = identifier
        self.expression = expression
        self.trueCodeBlock = trueCodeBlock
        self.elseCodeBlock = elseCodeBlock

    # __str__ :: None -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Identifier: {str(self.identifier)}\n{spacing}Expression: {str(self.expression)}\n{spacing}True: {str(self.trueCodeBlock)}\n{spacing}Else: {str(self.elseCodeBlock)}"

class Variable_Assignment(SimpleStatement):
    def __init__(self, nestLevel : int, identifier : Tokens.Identifier=None, expression : Expression=None):
        self.nestLevel = nestLevel
        self.identifier = identifier
        self.expression = expression

    # __str__ :: None -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Variable: {str(self.identifier)}\n{spacing}Value: {str(self.expression)}"

class Function_Call():
    def __init__(self, nestLevel : int, identifier : Tokens.Identifier=None, parameterList : Parameter_List=None) -> None:
        self.nestLevel = nestLevel
        self.identifier = identifier
        self.parameterList = parameterList
        
    # __str__ :: None -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Identifier: {self.identifier}\n{spacing}Parameter List: {str(self.parameterList)}"

class Return_Statement(SimpleStatement):
    def __init__(self, nestLevel : int, expression : Union[Expression, Function_Call]=None):
        self.nestLevel = nestLevel
        self.expression = expression

    # __str__ :: None -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Return Value: {str(self.expression)}"

class For_Loop():
    def __init__(self, nestLevel : int, startingValue : Union[Expression, int]=None, comparisonOperator : Tokens.Logic_Operator=None, body : Code_Block=None, increment : Union[Expression, int]=None, controlValue : Expression=None) -> None:
        self.nestLevel = nestLevel
        self.startingValue = startingValue
        self.comparisonOperator = comparisonOperator
        self.body = body
        self.increment = increment
        self.controlValue = controlValue
        
    # __str__ :: None -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Starting Value: {self.startingValue}\n{spacing}Comparison Operator: {self.comparisonOperator}\n{spacing}Loop Body: {str(self.body)}\n{spacing}Increment Value: {str(self.increment)}\n{spacing}Control Value: {str(self.controlValue)}"

class AST():
    def __init__(self, nestLevel : int, identifier : Tokens.Identifier=None, parameterList : Parameter_List=None, codeBlock : Code_Block=None) -> None:
        self.nestLevel = nestLevel
        self.identifier = identifier
        self.parameterList = parameterList
        self.codeBlock = codeBlock
        
    # __str__ :: None -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Identifier: {self.identifier}\n{spacing}Parameter List: {str(self.parameterList)}\n{spacing}Code Block: {str(self.codeBlock)}"
