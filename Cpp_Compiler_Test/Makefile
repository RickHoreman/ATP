#############################################################################
#
# Project Makefile
#
# (c) Wouter van Ooijen (www.voti.nl) 2016
#
# This file is in the public domain.
# 
#############################################################################
.PHONY = all

gcc := g++
ln := "..\..\i686-7.3.0-release-posix-dwarf-rt_v5-rev0\mingw32/bin/g++"
# source files in this project (main.cpp is automatically assumed)
SOURCES := ../asm/Sadge.asm

# header files in this project
HEADERS := 

# other places to look for files for this project
SEARCH  := 

SADGE := ../examples/unit_tests.painandsuffering

SADGEFLAGS := -DTC

cleanASM:
	del "..\asm\*.o"
	del "..\asm\*.asm"

deepclean:
	del "..\asm\*.o"
	del "..\asm\*.asm"
	del "..\Cpp_Compiler_Test\*.o"
	del "..\Cpp_Compiler_Test\*flags"
	del "..\Cpp_Compiler_Test\*.map"
	del "..\Cpp_Compiler_Test\*.ld"
	del "..\Cpp_Compiler_Test\bmptk_fixed_size_stack.c"

# make doesnt want to play nice so I had to put the full path to my python executable :/ (you'll have to change this for yourself, maybe for you just 'python' is enough)
../asm/Sadge.asm:
	@echo Compiling Sadge code
	C:\Users\rick2\AppData\Local\Programs\Python\Python39\python.exe ../source/Sadge.py $(SADGE) $(SADGEFLAGS)
	@echo Finished compiling Sadge code

# set RELATIVE to the next higher directory 
# and defer to the Makefile.due there
RELATIVE := $(RELATIVE)../..
BMPTK := $(RELATIVE)/bmptk
include $(RELATIVE)/Makefile.due
