import inspect

def unknownError(filename : str):
   print(f"Exited due to unhandled error at line {inspect.currentframe().f_back.f_lineno} in file {filename}")
   exit(69) 