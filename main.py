import os
from ply import lex, yacc
from classes.lexer import tokens, reserved, make_psuedocode_lexer
from classes.parser import make_pseudocode_parser
from classes.compiler import PseudocodeCompiler

# CIE Pseudocode compiler

EXAMPLE_1 = "PRINT 3+3"

EXAMPLE_2 = """
DECLARE x: INTEGER
x <- 2
IF x >= 2 THEN
   PRINT x
ELSE
    PRINT x+2 // test comment
ENDIF 
"""

RUN_AFTER_COMPILE = True

lexer = make_psuedocode_lexer()
parser = make_pseudocode_parser()
compiler = PseudocodeCompiler()


print("Testing EXAMPLE_2:")
compiler.reset()
compiler.ast = parser.parse(EXAMPLE_2, lexer=lexer)
c_code = compiler.compile_to_c()
print(c_code)

print("Calling GCC")
compiler.invoke_gcc()
print("Compiled successfully! \n Compiled binary is at temp/temp.exe")
print("Executing the binary")
if RUN_AFTER_COMPILE:
    print("=======OUTPUT=======")
    os.chdir('temp')
    os.system('temp.exe')
