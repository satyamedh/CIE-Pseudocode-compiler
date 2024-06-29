import os


class PseudocodeCompiler:

    binop_cond_psc_to_cpp = {
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

    datatypes_to_cpp = {
        'INTEGER': 'int',
        'STRING': 'char*',
        'BOOLEAN': 'bool'
    }

    def __init__(self, cpp_file: str = "temp/temp.cpp", output_file: str = "temp/temp"):
        self.ast = None
        self.cpp_code = ""

        self.cpp_file = cpp_file
        self.output_file = output_file
        self.variables = {}


    def walk(self, node):
        # node could be a tuple or a list of tuples
        if isinstance(node, tuple):
            if node[0] == 'binop':
                return f'({self.walk(node[2])} {self.binop_cond_psc_to_cpp[node[1]]} {self.walk(node[3])})'
            elif node[0] == 'number':
                return str(node[1])
            elif node[0] == 'string':
                return f'"{node[1]}"'
            elif node[0] == 'variable':
                return node[1]
            elif node[0] == 'assign':
                return f'{node[1]} = {self.walk(node[2])};'
            elif node[0] == 'print':
                return f'''
                std::cout << {self.walk(node[1])} << std::endl;                
                '''
            elif node[0] == 'input':
                # get the datatype of the variable
                datatype = self.variables[node[1]]
                if datatype == 'STRING' or datatype == 'INTEGER':
                    return f'std::cin >> {node[1]};'
                if datatype == 'BOOLEAN':
                    return f'''
                    char* {node[1]}_str = new char[10];
                    std::cin >> {node[1]}_str;
                    {node[1]} = string_to_bool({node[1]}_str);
                    free({node[1]}_str);
                    '''
            elif node[0] == 'if':
                return f'if ({self.walk(node[1])}) {{\n{self.walk(node[2])}\n}} else {{\n{self.walk(node[3])}\n}}'
            elif node[0] == 'if_no_else':
                return f'if ({self.walk(node[1])}) {{\n{self.walk(node[2])}\n}}'
            elif node[0] == 'for':
                return f'for (int {node[1]} = {self.walk(node[2])}; {node[1]} <= {self.walk(node[3])}; {node[1]}++) {{\n{self.walk(node[4])}\n}}'
            elif node[0] == 'condition':
                if node[1] == 'NOT':
                    return f'!{self.walk(node[2])}'
                return f'({self.walk(node[2])} {self.binop_cond_psc_to_cpp[node[1]]} {self.walk(node[3])})'
            elif node[0] == 'program':
                if not node[1]:
                    return ""
                return '\n'.join([self.walk(child) for child in node[1]])
            elif node[0] == 'declare':
                self.variables[node[1]] = node[2]
                return f'{self.datatypes_to_cpp[node[2]]} {node[1]};'
        elif isinstance(node, list):
            if not node:
                return ""
            return '\n'.join([self.walk(child) for child in node])
        else:
            raise ValueError(f"Unknown node type {node}")

    def compile_to_cpp(self):
        if self.ast is None:
            raise ValueError("AST is None")
        cpp_code = f"""
        #include <stdlib.h>
        #include <string.h>
        #include <iostream>
        
        // Helper functions
        bool string_to_bool(char* str) {{
            // convert the string to lowercase
            for (int i = 0; str[i]; i++) {{
                str[i] = tolower(str[i]);
            }}
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
        cpp_code = '\n'.join([line for line in cpp_code.split('\n') if line.strip()])
        # Remove trailing & leading spaces
        cpp_code = '\n'.join([line.strip() for line in cpp_code.split('\n')])

        # TODO: Indentaion

        self.cpp_code = cpp_code
        return cpp_code

    def write_to_file(self):
        # Make sure the directory exists
        try:
            os.mkdir(os.path.dirname(self.cpp_file))
        except FileExistsError:
            pass
        with open(self.cpp_file, 'w') as f:
            f.write(self.cpp_code)

    def invoke_gcc(self):
        # Make sure the directory exists
        try:
            os.mkdir(os.path.dirname(self.output_file))
        except FileExistsError:
            pass
        os.system(f'g++ {self.cpp_file} -o {self.output_file}')

    def reset(self):
        self.ast = None
        self.cpp_code = ""
