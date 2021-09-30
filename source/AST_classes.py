import Tokens

# class Code_Block:
#     # __str__ :: None -> String
#     def __str__(self) -> str:
#         return f"{self.__class__.__name__}."

class AST:
    def __init__(self, name : str="main") -> None:
        self.name = name
        self.codeBlock = Code_Block()
        self.parameters = Parameter_List()

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__}.\n  Name: {self.name}.\n{self.codeBlock.__str__()}\n{self.parameters.__str__()}"

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

class Code_Block():
    def __init__(self) -> None:
        self.code = []

    def append(self, statement : SimpleStatement):
        self.code.append(statement)

    # __str__ :: None -> String
    def __str__(self) -> str:
        codeStr = ""
        for item in self.code:
            codeStr += "\n  "
            codeStr += item.__str__()
        return f"{self.__class__.__name__}." + codeStr

class Parameter_List():
    def __init__(self) -> None:
        self.identifiers = []

    def append(self, identifier : Tokens.Identifier):
        self.identifiers.append(identifier)

    # __str__ :: None -> String
    def __str__(self) -> str:
        identifiersStr = ""
        for item in self.identifiers:
            identifiersStr += "\n  "
            identifiersStr += item.__str__()
        return f"{self.__class__.__name__}." + identifiersStr
