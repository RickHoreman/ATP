class Token:
    # __init__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        self.lineNr = lineNr
        self.charNr = charNr

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}."

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

class Assignment(Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Assignment_End(Operator):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Function_Definition(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Code_Block_Start(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Code_Block_End(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)