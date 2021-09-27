class Token:
    # __init__ :: Int -> Int -> None
    def __init__(self, lineNr : int, charNr : int) -> None:
        self.lineNr = lineNr
        self.charNr = charNr

    # __str__ :: None -> String
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}."