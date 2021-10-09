from Base_Token import Token

class For_Loop(Token):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Opening(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Starting_Value_Definition_Or_Increment_Definition(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Default_Starting_Value(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Comparison_Operator_Definition(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Comparison_Operator_Definition_End(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Body_Definition(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Body_Definition_End(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Default_Increment(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Default_Decrement(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Increment_Definition_End(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_Control_Value_Definition_End(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)

class For_Loop_End(For_Loop):
    def __init__(self, lineNr : int, charNr : int) -> None:
        super().__init__(lineNr, charNr)
