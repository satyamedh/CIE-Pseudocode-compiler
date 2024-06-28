import os
from ply import lex, yacc
from classes.lexer import tokens, reserved, make_psuedocode_lexer
from classes.parser import make_pseudocode_parser

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


# Test the parser
def test_parser(input_string):
    lexer.input(input_string)
    for tok in lexer:
        print(tok)
    result = parser.parse(input_string)
    print(result)


# print("Testing EXAMPLE_1:")
# test_parser(EXAMPLE_1)
#
# print("Testing EXAMPLE_2:")
# test_parser(EXAMPLE_2)

# Compile to C
# define a function to recursively walk the AST and generate C code

def walk(node):
    # node could be a tuple or a list of tuples
    if isinstance(node, tuple):
        if node[0] == 'binop':
            return f'({walk(node[2])} {node[1]} {walk(node[3])})'
        elif node[0] == 'number':
            return str(node[1])
        elif node[0] == 'variable':
            return node[1]
        elif node[0] == 'assign':
            return f'{node[1]} = {walk(node[2])};'
        elif node[0] == 'print':
            return f'printf("%d\\n", {walk(node[1])});'
        elif node[0] == 'if':
            return f'if ({walk(node[1])}) {{\n{walk(node[2])}\n}} else {{\n{walk(node[3])}\n}}'
        elif node[0] == 'condition':
            return f'({walk(node[2])} {node[1]} {walk(node[3])})'
        elif node[0] == 'program':
            return '\n'.join([walk(child) for child in node[1]])
        elif node[0] == 'declare':
            return f'int {node[1]};'
    elif isinstance(node, list):
        return '\n'.join([walk(child) for child in node])
    else:
        raise ValueError(f"Unknown node type {node}")

def compile_to_c(input_string):
    lexer.input(input_string)
    result = parser.parse(input_string, lexer=lexer)

    c_code = f"""
    #include <stdio.h>
    
    int main() {{
    {walk(result)}
    return 0;
    }}
    """

    # Prettify the code
    # Remove empty lines
    c_code = '\n'.join([line for line in c_code.split('\n') if line.strip()])
    # Remove trailing & leading spaces
    c_code = '\n'.join([line.strip() for line in c_code.split('\n')])

    # TODO: Indentaion

    return c_code

def invoke_gcc(c_code):
    try:
        os.mkdir('temp')
    except FileExistsError:
        pass
    with open('temp/temp.c', 'w') as f:
        f.write(c_code)

    os.system('gcc temp/temp.c -o temp/temp')


print("Testing EXAMPLE_2:")
c_code = compile_to_c(EXAMPLE_2)
print(c_code)

print("Calling GCC")
invoke_gcc(c_code)
print("Compiled successfully! \n Compiled binary is at temp/temp.exe")

print("Executing the binary")
if RUN_AFTER_COMPILE:
    print("=======OUTPUT=======")
    os.chdir('temp')
    os.system('temp.exe')
