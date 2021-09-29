import Tokens

# class Code_Block:
#     # __str__ :: None -> String
#     def __str__(self) -> str:
#         return f"{self.__class__.__name__}."

class AST:
    def __init__(self, name : str="main") -> None:
        self.name = name
        self.codeBlock = []
        self.args = []

    # __str__ :: None -> String
    def __str__(self) -> str:
        codeBlockStr = ""
        for item in self.codeBlock:
            codeBlockStr += "\n  "
            codeBlockStr += item.__str__()
        return f"{self.__class__.__name__}." + codeBlockStr

class SimpleStatement:
    # __init__ :: Int -> Int -> None
    # def __init__(self) -> None:

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

