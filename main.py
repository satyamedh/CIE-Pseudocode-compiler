import os
import argparse
from classes.lexer import make_psuedocode_lexer
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
arg_parser.add_argument("-d", "--debug", help="Debug output", action="store_true")
args = arg_parser.parse_args()

# Read the file
file = args.file
if not os.path.exists(file):
    print(f"File {file} does not exist")
    exit(1)

with open(file, 'r') as f:
    code = f.read()

# Lex and parse the code
print("Lexing and parsing")
lexer.input(code)
if args.debug:
    print("==== LEX ====")
    for tok in lexer:
        print(tok)
    lexer.input(code)
    print("==== PARSE ====")
ast = parser.parse(code, lexer=lexer)
if args.debug:
    print(ast)

# Compile the code
print("Compiling")
compiler.ast = ast
compiler.compile_to_cpp()
c_code = compiler.cpp_code
if args.debug:
    print("==== C CODE ====")
    print(c_code)

# Write and compile the C code
compiler.cpp_file = args.cfile or 'temp/temp.c'
compiler.output_file = args.output or 'temp/temp'

print("Writing to file")
compiler.write_to_file()
print("Compiling with gcc")
compiler.invoke_gcc()

# Run the compiled file if needed
if args.run:
    print("==== OUTPUT ====")
    os.chdir(os.path.dirname(compiler.output_file))
    os.system(os.path.basename(compiler.output_file))
