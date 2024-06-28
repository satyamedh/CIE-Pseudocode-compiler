import os
import argparse
from ply import lex, yacc
from classes.lexer import tokens, reserved, make_psuedocode_lexer
from classes.parser import make_pseudocode_parser
from classes.compiler import PseudocodeCompiler

# CIE Pseudocode compiler


lexer = make_psuedocode_lexer()
parser = make_pseudocode_parser()
compiler = PseudocodeCompiler()

# Get arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file", help="The file to compile")
arg_parser.add_argument("-o", "--output", help="The output file")
arg_parser.add_argument("-c", "--cfile", help="The C file to generate")
arg_parser.add_argument("-r", "--run", help="Run the compiled file", action="store_true")
args = arg_parser.parse_args()

# Read the file
file = args.file
if not os.path.exists(file):
    print(f"File {file} does not exist")
    exit(1)

with open(file, 'r') as f:
    code = f.read()

# Lex and parse the code
lexer.input(code)
ast = parser.parse(code, lexer=lexer)

# Compile the code
compiler.ast = ast
compiler.compile_to_c()
c_code = compiler.c_code

# Write and compile the C code
compiler.c_file = args.cfile or 'temp/temp.c'
compiler.output_file = args.output or 'temp/temp'

compiler.write_to_file()
compiler.invoke_gcc()

# Run the compiled file if needed

if args.run:
    os.system(f'{compiler.output_file}')





