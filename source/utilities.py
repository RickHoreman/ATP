import inspect

# unkownError :: String -> None
def unknownError(filename : str):
    print(f"Exited due to unhandled error at line {inspect.currentframe().f_back.f_lineno} in file {filename}")
    exit(69) 

# space :: Integer -> String
def space( repeatCount : int):
    if (repeatCount <= 0):
        return ""
    return "|   " + space(repeatCount - 1)