import os
from ply import lex, yacc

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

reserved = {
    'DECLARE': 'DECLARE',
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'ENDIF': 'ENDIF',
    'PRINT': 'PRINT',
    'INTEGER': 'INTEGER'
}

tokens = (
             "ASSIGNMENT",
             "COLON",
             "PLUS",
             "MINUS",
             "MULTIPLY",
             "DIVIDE",
             "GREATER_THAN",
             "LESS_THAN",
             "GREATER_THAN_EQUAL",
             "LESS_THAN_EQUAL",
             "EQUAL",
             "VARIABLE",
             "NUMBER"
         ) + tuple(reserved.values())

t_ignore = r'   '

t_GREATER_THAN_EQUAL = r'>='
t_LESS_THAN_EQUAL = r'<='

t_EQUAL = r'='

t_GREATER_THAN = r'>'
t_LESS_THAN = r'<'

t_ASSIGNMENT = r'<-'
t_COLON = r'\:'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'


def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)


def t_COMMENT(t):
    r'\/\/.*'
    pass
    # No return value. Token discarded


lexer = lex.lex()


# --- Parser

def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])


def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement_declare(p):
    '''statement : DECLARE VARIABLE COLON INTEGER'''
    p[0] = ('declare', p[2], p[4])


def p_statement_assign(p):
    '''statement : VARIABLE ASSIGNMENT expression'''
    p[0] = ('assign', p[1], p[3])


def p_statement_if(p):
    '''statement : IF condition THEN statement_list ELSE statement_list ENDIF'''
    p[0] = ('if', p[2], p[4], p[6])


def p_statement_print(p):
    '''statement : PRINT expression'''
    p[0] = ('print', p[2])


def p_condition(p):
    '''condition : expression GREATER_THAN expression
                 | expression LESS_THAN expression
                 | expression GREATER_THAN_EQUAL expression
                 | expression LESS_THAN_EQUAL expression
                 | expression EQUAL expression'''
    p[0] = ('condition', p[2], p[1], p[3])


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression'''
    p[0] = ('binop', p[2], p[1], p[3])


def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('number', p[1])


def p_expression_variable(p):
    '''expression : VARIABLE'''
    p[0] = ('variable', p[1])


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


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
    result = parser.parse(input_string)

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


