import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def remove_quotes(text):
    if text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    elif text[0] == "'" and text[-1] == "'":
        return text[1:-1]
    return text

def make_string_variable_friendly(text):
    text = text.replace('.', '_')
    text = text.replace('/', '_')
    return text
