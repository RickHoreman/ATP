import Tokens
from Base_Token import Token
from Tokens import Function_Definition

Integer_Assignment = [Tokens.Identifier, Tokens.Assignment, Tokens.Integer, Tokens.Assignment_End]
Function_Definition_Start = [Tokens.Function_Definition, Tokens.Identifier, Tokens.Parameter_List_Open]
Parameter_List_Item = [Tokens.Identifier, Tokens.Parameter_Seperator]
Parameter_List_Last_Item = [Tokens.Identifier, Tokens.Parameter_List_Close]

