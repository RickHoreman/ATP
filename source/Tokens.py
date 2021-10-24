from Base_Token import Token

class Value(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        self.value = None
        super().__init__(lineNr, charNr)

class Boolean(Value):
    def __init__(self, lineNr : int, charNr : int, value : bool) -> None:
        super().__init__(lineNr, charNr)
        self.value = value

    # __str__ :: Boolean -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}, with value {self.value}"

class Integer(Value):
    def __init__(self, lineNr : int, charNr : int, value : int) -> None:
        super().__init__(lineNr, charNr)
        self.value = value

    # __str__ :: Tokens.Integer -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}, with value {self.value}"

class Identifier(Value):
    def __init__(self, lineNr : int, charNr : int, name : str) -> None:
        super().__init__(lineNr, charNr)
        self.name = name

    # __str__ :: Identifier -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}, with name {self.name}"

class Operator(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Logic_Operator(Operator):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Assignment(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Assignment_End(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Addition(Operator):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Subtraction(Operator):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Greater_Than_Or_Equal(Logic_Operator):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Smaller_Than_Or_Equal(Logic_Operator):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Greater_Than(Logic_Operator):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Smaller_Than(Logic_Operator):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Expression_Bracket_Open(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Expression_Bracket_Close(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Function_Definition(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Code_Block_Open(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Code_Block_Close(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Parameter_List_Open(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Parameter_List_Close(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Parameter_Seperator(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Endline(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class If_Statement(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class If_Statement_Continuation(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Else(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Return_Statement(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Print_Statement(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)
