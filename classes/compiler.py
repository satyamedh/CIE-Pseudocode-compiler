import os
import random
import subprocess


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
        'BOOLEAN': 'bool',
        'CHAR': 'char',
        'REAL': 'float'
    }

    declare_defaults = {
        'INTEGER': 0,
        'STRING': '""',
        'BOOLEAN': 'false',
        'CHAR': "' '",
        'REAL': 0.0
    }

    def __init__(self, cpp_file: str = "temp/temp.cpp", output_file: str = "temp/temp", random_seed: int = 42):
        self.ast = None
        self.cpp_code = ""

        self.cpp_file = cpp_file
        self.output_file = output_file

        self.variables = {}
        self.procedures = []

        random.seed(random_seed)

        self.generated_randoms = []

        self.main_body_flag = True

    def generate_random(self):
        random_num = random.randint(0, 1000)
        while random_num in self.generated_randoms:
            random_num = random.randint(0, 1000)
        self.generated_randoms.append(random_num)
        return random_num

    def set_main_body_flag(self, flag):
        self.main_body_flag = flag
        return ''


    def walk(self, node):
        # node could be a tuple or a list of tuples
        if isinstance(node, tuple):
            if node[0] == 'binop':
                if node[1] == 'NOT':
                    return f'!{self.walk(node[2])}'
                return f'({self.walk(node[2])} {self.binop_cond_psc_to_cpp[node[1]]} {self.walk(node[3])})'
            elif node[0] == 'number':
                return str(node[1])
            elif node[0] == 'string':
                return f'"{node[1]}"'
            elif node[0] == 'char':
                return f"'{node[1]}'"
            elif node[0] == 'variable':
                return node[1]
            elif node[0] == 'boolean':
                return str(node[1]).lower()
            elif node[0] == 'assign':
                return f'{node[1]} = {self.walk(node[2])};'
            elif node[0] == 'print':
                return f'''
                std::cout << {self.walk(node[1])} << std::endl;                
                '''
            elif node[0] == 'procedure_no_param':
                if self.main_body_flag:
                    self.procedures.append(node)
                    return ''
                else:
                    return f'''
                    void {node[1]}() {{
                        {self.walk(node[2])}
                    }}
                    '''
            elif node[0] == 'call_procedure_no_param':
                return f'{node[1]}();'
            elif node[0] == 'input':
                # get the datatype of the variable
                datatype = self.variables[node[1]]
                if datatype == 'STRING' or datatype == 'INTEGER' or datatype == 'REAL':
                    return f'std::cin >> {node[1]};'
                if datatype == 'BOOLEAN':
                    return f'''
                    std::string {node[1]}_str;
                    std::cin >> {node[1]}_str;
                    {node[1]} = string_to_bool({node[1]}_str);
                    '''
            elif node[0] == 'if':
                return f'if ({self.walk(node[1])}) {{\n{self.walk(node[2])}\n}} else {{\n{self.walk(node[3])}\n}}'
            elif node[0] == 'if_no_else':
                return f'if ({self.walk(node[1])}) {{\n{self.walk(node[2])}\n}}'
            elif node[0] == 'repeat':
                random_num = self.generate_random()
                return f'''
                bool {node[0]}_cond_{random_num} = true;
                while ({node[0]}_cond_{random_num}) {{
                    {self.walk(node[1])}
                    {node[0]}_cond_{random_num} = !({self.walk(node[2])});
                }}
                '''
            elif node[0] == 'while':
                return f'while ({self.walk(node[1])}) {{\n{self.walk(node[2])}\n}}'
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
                return f'{self.datatypes_to_cpp[node[2]]} {node[1]} = {self.declare_defaults[node[2]]};'
        elif isinstance(node, list):
            if not node:
                return ""
            return '\n'.join([self.walk(child) for child in node])
        else:
            raise ValueError(f"Unknown node type {node}")

    def compile_to_cpp(self):
        if self.ast is None:
            raise ValueError("AST is None")

        main_body_code = self.walk(self.ast)

        self.set_main_body_flag(False)
        procedure_code = '\n'.join([self.walk(proc) for proc in self.procedures])

        cpp_code = f"""
        #include <cstdlib>
        #include <cstring>
        #include <iostream>
        #include <cctype>
        
        // Helper functions
        bool string_to_bool(std::string str) {{
            for (char &c : str) {{
                c = std::tolower(c);
            }}
        return str == "true";
        }}
        
        {procedure_code}        
        
        int main() {{
            {main_body_code}
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

        process = subprocess.Popen(['g++', self.cpp_file, '-o', self.output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if stderr:
            return False, stderr
        return True, None


    def reset(self):
        self.ast = None
        self.cpp_code = ""
