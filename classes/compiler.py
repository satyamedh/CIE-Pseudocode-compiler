import os


class PseudocodeCompiler:

    binop_cond_psc_to_c = {
        "=": "==",
        "<>": "!=",
        "<": "<",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
        "+": "+",
        "-": "-",
        "*": "*",
        "/": "/",
        "MOD": "%",
        "DIV": "/",
        "AND": "&&",
        "OR": "||",
        "NOT": "!"
    }

    datatype_for_print = {
        'number': '%d',
        'string': '%s',
        'INTEGER': '%d',
        'STRING': '%s',
    }

    datatypes_to_c = {
        'INTEGER': 'int',
        'STRING': 'char*',
        'BOOLEAN': 'bool'
    }

    def __init__(self, c_file: str = "temp/temp.c", output_file: str = "temp/temp"):
        self.ast = None
        self.c_code = ""

        self.c_file = c_file
        self.output_file = output_file
        self.variables = {}


    def walk(self, node):
        # node could be a tuple or a list of tuples
        if isinstance(node, tuple):
            if node[0] == 'binop':
                return f'({self.walk(node[2])} {self.binop_cond_psc_to_c[node[1]]} {self.walk(node[3])})'
            elif node[0] == 'number':
                return str(node[1])
            elif node[0] == 'string':
                return f'"{node[1]}"'
            elif node[0] == 'variable':
                return node[1]
            elif node[0] == 'assign':
                return f'{node[1]} = {self.walk(node[2])};'
            elif node[0] == 'print':
                if node[1][0] == 'string':
                    return f'printf("{self.datatype_for_print[node[1][0]]}\\n", {self.walk(node[1])});'
                return f'printf("%d\\n", {self.walk(node[1])});'
            elif node[0] == 'input':
                # get the datatype of the variable
                datatype = self.variables[node[1]]
                if datatype == 'STRING' or datatype == 'INTEGER':
                    return f'scanf("{self.datatype_for_print[datatype]}", &{node[1]});'
                if datatype == 'BOOLEAN':
                    return f'''
                    char* {node[1]}_str = malloc(10);
                    scanf("%s", {node[1]}_str);
                    {node[1]} = string_to_bool({node[1]}_str);
                    // deallocate the memory
                    free({node[1]}_str);'''
            elif node[0] == 'if':
                return f'if ({self.walk(node[1])}) {{\n{self.walk(node[2])}\n}} else {{\n{self.walk(node[3])}\n}}'
            elif node[0] == 'if_no_else':
                return f'if ({self.walk(node[1])}) {{\n{self.walk(node[2])}\n}}'
            elif node[0] == 'for':
                return f'for (int {node[1]} = {self.walk(node[2])}; {node[1]} <= {self.walk(node[3])}; {node[1]}++) {{\n{self.walk(node[4])}\n}}'
            elif node[0] == 'condition':
                if node[1] == 'NOT':
                    return f'!{self.walk(node[2])}'
                return f'({self.walk(node[2])} {self.binop_cond_psc_to_c[node[1]]} {self.walk(node[3])})'
            elif node[0] == 'program':
                if not node[1]:
                    return ""
                return '\n'.join([self.walk(child) for child in node[1]])
            elif node[0] == 'declare':
                self.variables[node[1]] = node[2]
                return f'{self.datatypes_to_c[node[2]]} {node[1]};'
        elif isinstance(node, list):
            if not node:
                return ""
            return '\n'.join([self.walk(child) for child in node])
        else:
            raise ValueError(f"Unknown node type {node}")

    def compile_to_c(self):
        if self.ast is None:
            raise ValueError("AST is None")
        c_code = f"""
        #include <stdio.h>
        #include <stdbool.h> 
        #include <stdlib.h>
        #include <string.h>
        
        // Helper functions
        bool string_to_bool(char* str) {{
            if (strcmp(str, "true") == 0) {{
                return true;
            }}
            return false;
        }}
        
        
        int main() {{
        {self.walk(self.ast)}
        return 0;
        }}
        """

        # Prettify the code
        # Remove empty lines
        c_code = '\n'.join([line for line in c_code.split('\n') if line.strip()])
        # Remove trailing & leading spaces
        c_code = '\n'.join([line.strip() for line in c_code.split('\n')])

        # TODO: Indentaion

        self.c_code = c_code
        return c_code

    def write_to_file(self):
        # Make sure the directory exists
        try:
            os.mkdir(os.path.dirname(self.c_file))
        except FileExistsError:
            pass
        with open(self.c_file, 'w') as f:
            f.write(self.c_code)

    def invoke_gcc(self):
        # Make sure the directory exists
        try:
            os.mkdir(os.path.dirname(self.output_file))
        except FileExistsError:
            pass
        os.system(f'gcc {self.c_file} -o {self.output_file}')

    def reset(self):
        self.ast = None
        self.c_code = ""
