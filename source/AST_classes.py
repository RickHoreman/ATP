import Tokens
from typing import Union, List
from utilities import space

class Simple_Statement:
    # __str__ :: Simple_Statement -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

class Expression_Base(): # Had to make this so that I could do the typing on Expression's __init__ :/
    # __str__ :: Expression_Base -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

class Expression(Expression_Base):
    def __init__(self, nestLevel : int, left : Union[Expression_Base, Tokens.Value]=None, operator : Tokens.Operator=None, right : Union[Expression_Base, Tokens.Value]=None) -> None:
        self.nestLevel = nestLevel
        self.left = left
        self.operator = operator
        self.right = right

    # __str__ :: Expression -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Left: {str(self.left)}\n{spacing}Operator: {str(self.operator)}\n{spacing}Right: {str(self.right)}"

class Code_Block(Simple_Statement):
    def __init__(self, nestLevel : int) -> None:
        self.nestLevel = nestLevel
        self.code = []

    # append :: Code_Block -> Simple_Statement -> Code_Block
    def append(self, statement : Simple_Statement):
        self.code.append(statement)

    # __str__ :: Code_Block -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        statestr = ''.join(map(lambda st: "\n" + spacing + str(st), self.code))
        return f"{self.__class__.__name__}" + statestr

class Parameter_List():
    def __init__(self, nestLevel : int) -> None:
        self.nestLevel = nestLevel
        self.values = []

    # append :: Parameter_List -> Tokens.Value -> Parameter_List
    def append(self, value : Tokens.Value):
        self.values.append(value)

    # pop :: Parameter_List -> (Tokens.Value, Parameter_List)
    def pop(self) -> Tokens.Value:
        return self.values.pop()

    # __str__ :: Parameter_List -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        statestr = ''.join(map(lambda st: "\n" + spacing + str(st), self.values))
        return f"{self.__class__.__name__}" + statestr

class If_Statement(Simple_Statement):
    def __init__(self, nestLevel : int, identifier : Tokens.Identifier=None, expression : Expression=None, trueCodeBlock : Code_Block=None, elseCodeBlock : Code_Block=None):
        self.nestLevel = nestLevel
        self.identifier = identifier
        self.expression = expression
        self.trueCodeBlock = trueCodeBlock
        self.elseCodeBlock = elseCodeBlock

    # __str__ :: If_Statement -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Identifier: {str(self.identifier)}\n{spacing}Expression: {str(self.expression)}\n{spacing}True: {str(self.trueCodeBlock)}\n{spacing}Else: {str(self.elseCodeBlock)}"

class Variable_Assignment(Simple_Statement):
    def __init__(self, nestLevel : int, identifier : Tokens.Identifier=None, expression : Expression=None):
        self.nestLevel = nestLevel
        self.identifier = identifier
        self.expression = expression

    # __str__ :: Variable_Assignment -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Variable: {str(self.identifier)}\n{spacing}Value: {str(self.expression)}"

class Function_Call():
    def __init__(self, nestLevel : int, identifier : Tokens.Identifier=None, parameterList : Parameter_List=None) -> None:
        self.nestLevel = nestLevel
        self.identifier = identifier
        self.parameterList = parameterList
        
    # __str__ :: Function_Call -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Identifier: {self.identifier}\n{spacing}Parameter List: {str(self.parameterList)}"

class Return_Statement(Simple_Statement):
    def __init__(self, nestLevel : int, expression : Union[Expression, Function_Call]=None):
        self.nestLevel = nestLevel
        self.expression = expression

    # __str__ :: Return_Statement -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Return Value: {str(self.expression)}"

class Print_Statement(Simple_Statement):
    def __init__(self, nestLevel : int, expression : Union[Expression, Function_Call]=None):
        self.nestLevel = nestLevel
        self.expression = expression

    # __str__ :: Print_Statement -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Expression: {str(self.expression)}"

class For_Loop():
    def __init__(self, nestLevel : int, startingValue : Union[Expression, int]=None, comparisonOperator : Tokens.Logic_Operator=None, body : Code_Block=None, increment : Union[Expression, int]=None, controlValue : Expression=None) -> None:
        self.nestLevel = nestLevel
        self.startingValue = startingValue
        self.comparisonOperator = comparisonOperator
        self.body = body
        self.increment = increment
        self.controlValue = controlValue
        
    # __str__ :: For_Loop -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Starting Value: {self.startingValue}\n{spacing}Comparison Operator: {self.comparisonOperator}\n{spacing}Loop Body: {str(self.body)}\n{spacing}Increment Value: {str(self.increment)}\n{spacing}Control Value: {str(self.controlValue)}"

class AST():
    def __init__(self, nestLevel : int, identifier : Tokens.Identifier=None, parameterList : Parameter_List=None, codeBlock : Code_Block=None) -> None:
        self.nestLevel = nestLevel
        self.identifier = identifier
        self.parameterList = parameterList
        self.codeBlock = codeBlock
        
    # __str__ :: AST -> String
    def __str__(self) -> str:
        spacing = space(self.nestLevel)
        return f"{self.__class__.__name__}\n{spacing}Identifier: {self.identifier}\n{spacing}Parameter List: {str(self.parameterList)}\n{spacing}Code Block: {str(self.codeBlock)}"
