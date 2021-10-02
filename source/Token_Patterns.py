import Tokens
import For_Loop_Tokens as FL
from Base_Token import Token

Assignment_Or_If_Statement = [Tokens.Identifier, Tokens.Assignment]
Assignment_End = [Tokens.Assignment_End]
If_Statement_End = [Tokens.If_Statement, Tokens.If_Statement_Continuation, Tokens.Code_Block_Open]
Else = [Tokens.Else, Tokens.Code_Block_Open]
Function_Definition_Start = [Tokens.Function_Definition, Tokens.Identifier, Tokens.Parameter_List_Open]
Parameter_List_Item = [Tokens.Identifier, Tokens.Parameter_Seperator]
Parameter_List_Last_Item = [Tokens.Identifier, Tokens.Parameter_List_Close]
Function_Call = [Tokens.Identifier, Tokens.Parameter_List_Open]

For_Loop_Opening = [FL.For_Loop_Opening]
For_Loop_Default_Starting_Value = [FL.For_Loop_Default_Starting_Value, FL.For_Loop_Comparison_Operator_Definition]
For_Loop_Starting_Value_Definition = [FL.For_Loop_Starting_Value_Definition_Or_Increment_Definition]
For_Loop_Starting_Value_Definition_End = [FL.For_Loop_Comparison_Operator_Definition]
For_Loop_Body_Definition = [FL.For_Loop_Comparison_Operator_Definition_End, FL.For_Loop_Body_Definition, Tokens.Code_Block_Open]
For_Loop_Body_Definition_End = [FL.For_Loop_Body_Definition_End]
For_Loop_Default_Increment = [FL.For_Loop_Default_Increment]
For_Loop_Default_Decrement = [FL.For_Loop_Default_Decrement]
For_Loop_Increment_Definition = [FL.For_Loop_Starting_Value_Definition_Or_Increment_Definition]
For_Loop_Increment_Definition_End = [FL.For_Loop_Increment_Definition_End]
For_Loop_End = [FL.For_Loop_Control_Value_Definition_End, FL.For_Loop_End]
