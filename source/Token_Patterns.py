import Tokens
from Base_Token import Token
from Tokens import Function_Definition

Assignment_Or_If_Statement = [Tokens.Identifier, Tokens.Assignment]
Assignment_End = [Tokens.Assignment_End]
If_Statement_End = [Tokens.If_Statement, Tokens.If_Statement_Continuation, Tokens.Code_Block_Open]
Else = [Tokens.Else, Tokens.Code_Block_Open]
Function_Definition_Start = [Tokens.Function_Definition, Tokens.Identifier, Tokens.Parameter_List_Open]
Parameter_List_Item = [Tokens.Identifier, Tokens.Parameter_Seperator]
Parameter_List_Last_Item = [Tokens.Identifier, Tokens.Parameter_List_Close]

