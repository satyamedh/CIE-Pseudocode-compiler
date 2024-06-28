import ply.lex as lex

reserved = {
    'DECLARE': 'DECLARE',
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'ENDIF': 'ENDIF',
    'OUTPUT': 'PRINT',
    'INTEGER': 'INTEGER',
    'STRING': 'STRING',
    'INPUT': 'INPUT',
    'MOD': 'MOD',
    'DIV': 'DIV',
    'FOR': 'FOR',
    'TO': 'TO',
    'NEXT': 'NEXT',
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
    "NUMBER",
    "DOUBLE_QUOTE",
    "SINGLE_QUOTE",
    "STRING_DATA"
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

    t_DOUBLE_QUOTE = r'\"'
    t_SINGLE_QUOTE = r'\''

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

    def t_STRING_DATA(t):
        r"""(\"([^\\\n]|(\\.))*?\")|(\''([^\\\n]|(\\.))*?\')"""
        t.type = 'STRING_DATA'
        t.value = t.value[1:-1]
        return t

    return lex.lex()
