import importlib
import os
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


def dynamic_import(module_name, module_path):
    # import the function from tests/solutions/{file_name}.py
    sys.path.append(module_path)
    module = importlib.import_module(module_name)

    return module
