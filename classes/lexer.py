import ply.lex as lex

reserved = {
    'DECLARE': 'DECLARE',
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'ENDIF': 'ENDIF',
    'PRINT': 'PRINT',
    'INTEGER': 'INTEGER',
    'INPUT': 'INPUT',
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


def make_psuedocode_lexer():
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

    def __init__(self):
        self.lexer = None

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

    return lex.lex()
