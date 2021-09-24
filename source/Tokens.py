class Token:
    # __init__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        self.lineNr = lineNr
        self.charNr = charNr

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}"

class Primitive_Type(Token):
    # __init__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Integer_Type(Primitive_Type):
    # __init__ :: Int -> Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class Constant(Token):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)
        self.value = None

class Integer_Constant(Constant):
    # __innit__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int, value : int) -> None:
        super().__init__(lineNr, charNr)
        self.value = value

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}, with value {self.value}"