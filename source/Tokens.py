from Base_Token import Token

### UNUSED
# class Primitive_Type(Token): 
#     # __init__ :: Int -> Int -> None
#     def __init__(self, lineNr : int, charNr : int) -> None:
#         super().__init__(lineNr, charNr)
#
# class Integer_Type(Primitive_Type):
#     # __init__ :: Int -> Int -> Int -> None
#     def __init__(self, lineNr : int, charNr : int) -> None:
#         super().__init__(lineNr, charNr)
###

class Boolean(Token):
    # __innit__ :: Int -> Int -> Bool -> None
    def __init__(self, lineNr : int, charNr : int, value : bool) -> None:
        super().__init__(lineNr, charNr)
        self.value = value

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}, with value {self.value}."

class Integer(Token):
    # __innit__ :: Int -> Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int, value : int) -> None:
        super().__init__(lineNr, charNr)
        self.value = value

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}, with value {self.value}."

class Identifier(Token):
    # __innit__ :: Int -> Int -> String -> None
    def __init__(self, lineNr : int, charNr : int, name : str) -> None:
        super().__init__(lineNr, charNr)
        self.name = name

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}, with name {self.name}."

class Operator(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Logic_Operator(Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Assignment(Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Assignment_End(Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Addition(Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Subtraction(Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Greater_Than_Or_Equal(Logic_Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Smaller_Than_Or_Equal(Logic_Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Greater_Than(Logic_Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Smaller_Than(Logic_Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Function_Definition(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Code_Block_Open(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Code_Block_Close(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Parameter_List_Open(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Parameter_List_Close(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Parameter_Seperator(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Endline(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class If_Statement(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class If_Statement_Continuation(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Else(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Return_Statement(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)
