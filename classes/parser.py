from ply.yacc import yacc
from classes.lexer import tokens, reserved


def make_pseudocode_parser():
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

    def p_data_type(p):
        '''data_type : INTEGER
                     | STRING
                     | BOOLEAN
                     | CHAR
                     | REAL'''
        p[0] = p[1]

    def p_procedure_no_params(p):
        '''statement : PROCEDURE VARIABLE OPEN_BRACKET CLOSE_BRACKET statement_list ENDPROCEDURE'''
        p[0] = ('procedure_no_param', p[2], p[5])

    def p_call_procedure_no_param(p):
        '''statement : CALL VARIABLE OPEN_BRACKET CLOSE_BRACKET'''
        p[0] = ('call_procedure_no_param', p[2])


    def p_statement_declare(p):
        '''statement : DECLARE VARIABLE COLON data_type'''
        p[0] = ('declare', p[2], p[4])

    def p_parameter(p):
        '''parameter : VARIABLE COLON data_type'''
        p[0] = ('parameter', p[1], p[3])

    def p_parameters(p):
        '''parameters : parameter
                      | parameters COMMA parameter'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_function_with_params(p):
        '''statement : FUNCTION VARIABLE OPEN_BRACKET parameters CLOSE_BRACKET RETURNS data_type statement_list ENDFUNCTION'''
        p[0] = ('function_with_params', p[2], p[4], p[7], p[8])

    def p_function_no_params(p):
        '''statement : FUNCTION VARIABLE OPEN_BRACKET CLOSE_BRACKET RETURNS data_type statement_list ENDFUNCTION'''
        p[0] = ('function_no_params', p[2], p[6], p[7])

    def p_procedure_with_params(p):
        '''statement : PROCEDURE VARIABLE OPEN_BRACKET parameters CLOSE_BRACKET statement_list ENDPROCEDURE'''
        p[0] = ('procedure_with_params', p[2], p[4], p[6])

    def p_call_procedure_with_params(p):
        '''statement : CALL VARIABLE OPEN_BRACKET expression_list CLOSE_BRACKET'''
        p[0] = ('call_procedure_with_params', p[2], p[4])


    def p_return_statement(p):
        '''statement : RETURN expression'''
        p[0] = ('return', p[2])

    def p_expression_list(p):
        '''expression_list : expression
                           | expression_list COMMA expression'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_run_function_with_params(p):
        '''expression : VARIABLE OPEN_BRACKET expression_list CLOSE_BRACKET
                        | LENGTH OPEN_BRACKET expression_list CLOSE_BRACKET
                        | RIGHT OPEN_BRACKET expression_list CLOSE_BRACKET
                        | LEFT OPEN_BRACKET expression_list CLOSE_BRACKET
                        | MID OPEN_BRACKET expression_list CLOSE_BRACKET
                        | LCASE OPEN_BRACKET expression_list CLOSE_BRACKET
                        | UCASE OPEN_BRACKET expression_list CLOSE_BRACKET

        '''

        p[0] = ('run_function_with_params', p[1], p[3])

    def p_run_function_no_params(p):
        '''expression : VARIABLE OPEN_BRACKET CLOSE_BRACKET'''
        p[0] = ('run_function_no_params', p[1])

    def p_statement_for(p):
        '''statement : FOR VARIABLE ASSIGNMENT expression TO expression statement_list NEXT VARIABLE'''
        p[0] = ('for', p[2], p[4], p[6], p[7])

    def p_statement_repeat(p):
        '''statement : REPEAT statement_list UNTIL expression'''
        p[0] = ('repeat', p[2], p[4])

    def p_statement_assign(p):
        '''statement : VARIABLE ASSIGNMENT expression'''
        p[0] = ('assign', p[1], p[3])

    def p_statement_if(p):
        '''statement : IF expression THEN statement_list ELSE statement_list ENDIF'''
        p[0] = ('if', p[2], p[4], p[6])

    def p_statement_if_no_else(p):
        '''statement : IF expression THEN statement_list ENDIF'''
        p[0] = ('if_no_else', p[2], p[4])

    def p_statement_while(p):
        '''statement : WHILE expression statement_list ENDWHILE'''
        p[0] = ('while', p[2], p[3])

    def p_statement_print_multiple(p):
        '''statement : PRINT expression_list'''
        p[0] = ('print_multiple', p[2])

    def p_statement_print(p):
        '''statement : PRINT expression'''
        p[0] = ('print', p[2])

    def p_statement_input(p):
        '''statement :  INPUT VARIABLE'''
        p[0] = ('input', p[2])

    def p_expression_binop(p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression MULTIPLY expression
                      | expression DIVIDE expression
                      | expression MOD expression
                      | expression DIV expression
                      | expression AND expression
                      | expression OR expression
                      | expression EQUAL expression
                      | expression GREATER_THAN expression
                      | expression LESS_THAN expression
                      | expression GREATER_THAN_EQUAL expression
                      | expression LESS_THAN_EQUAL expression
                      | expression NOT_EQUAL expression
                      | NOT expression
                      | OPEN_BRACKET expression CLOSE_BRACKET
                      | expression CONCATENATE expression
                      '''
        if len(p) == 4:
            if p[1] == '(':
                p[0] = p[2]
            else:
                p[0] = ('binop', p[2], p[1], p[3])
        elif len(p) == 3:
            p[0] = ('binop', p[1], p[2])


    def p_expression_number(p):
        '''expression : NUMBER'''
        p[0] = ('number', p[1])

    def p_expression_real_number(p):
        '''expression : REAL_NUMBER'''
        p[0] = ('number', p[1])

    def p_expression_variable(p):
        '''expression : VARIABLE'''
        p[0] = ('variable', p[1])

    def p_expression_string(p):
        '''expression : STRING_DATA'''
        p[0] = ('string', p[1])

    def p_expression_char(p):
        '''expression : CHAR_DATA'''
        p[0] = ('char', p[1])

    def p_expression_boolean(p):
        '''expression : TRUE
                      | FALSE'''
        p[0] = ('boolean', p[1])

    def p_error(p):
        if p:
            print(f"Syntax error at '{p.value}' at line {p.lineno} column {p.lexpos}")
        else:
            print("Syntax error at EOF")

    return yacc()
