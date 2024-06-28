import os


class PseudocodeCompiler:

    def __init__(self, c_file: str = "temp/temp.c", output_file: str = "temp/temp"):
        self.ast = None
        self.c_code = ""

        self.c_file = c_file
        self.output_file = output_file

    def walk(self, node):
        # node could be a tuple or a list of tuples
        if isinstance(node, tuple):
            if node[0] == 'binop':
                return f'({self.walk(node[2])} {node[1]} {self.walk(node[3])})'
            elif node[0] == 'number':
                return str(node[1])
            elif node[0] == 'variable':
                return node[1]
            elif node[0] == 'assign':
                return f'{node[1]} = {self.walk(node[2])};'
            elif node[0] == 'print':
                return f'printf("%d\\n", {self.walk(node[1])});'
            elif node[0] == 'input':
                return f'scanf("%d", &{node[1]});'
            elif node[0] == 'if':
                return f'if ({self.walk(node[1])}) {{\n{self.walk(node[2])}\n}} else {{\n{self.walk(node[3])}\n}}'
            elif node[0] == 'condition':
                return f'({self.walk(node[2])} {node[1]} {self.walk(node[3])})'
            elif node[0] == 'program':
                return '\n'.join([self.walk(child) for child in node[1]])
            elif node[0] == 'declare':
                return f'int {node[1]};'
        elif isinstance(node, list):
            return '\n'.join([self.walk(child) for child in node])
        else:
            raise ValueError(f"Unknown node type {node}")

    def compile_to_c(self):

        c_code = f"""
        #include <stdio.h>

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
