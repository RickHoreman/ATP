class Token:
    def __init__(self, lineNr : int, charNr : int) -> None:
        self.lineNr = lineNr
        self.charNr = charNr

    # __str__ :: Token -> String
    def __str__(self) -> str: # All other tokens inherit this, unless they overwrite it.
        return f"{self.__class__.__name__} at Line {self.lineNr}, Char {self.charNr}"
    