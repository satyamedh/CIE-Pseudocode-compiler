import os
import importlib
import shutil
import subprocess
import json
import sys

from classes.general_functions import dynamic_import


def test_program(file_name):
    try:
        solutions = json.load(open(f'tests/solutions/{file_name}.json'))
    except FileNotFoundError:
        print(f"No solutions found for {file_name}")
        sys.exit(2)

    # the solutions are stored in the trials variable
    # each trial is a list of inputs and expected outputs

    # Delete the temp directory
    shutil.rmtree('temp', ignore_errors=True)

    # run the main.py file with the input
    # os.system(f'python main.py tests/{file_name}.psc -o temp/temp -c temp/temp.c')
    compiler_process = subprocess.Popen(['python', 'main.py', f'tests/{file_name}.psc', '-o', 'temp/temp', '-c',
                                         'temp/temp.c'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = compiler_process.communicate()
    # get exit code
    result = compiler_process.returncode
    if result != 0:
        print("====================================")
        print(f"Compilation might've failed for {file_name}")
        print("==== STDOUT ====")
        print(stdout)
        print("==== STDERR ====")
        print(stderr)
        print("====================================")
        sys.exit(-1)

    functiona = None

    custom_test_function = False
    if "function" in solutions:
        # import the function from tests/solutions/{file_name}.py
        module = dynamic_import(file_name, 'tests/solutions')
        functiona = getattr(module, "test")
        custom_test_function = True


    for index, trial in enumerate(solutions['trials']):
        input_data = str(trial[0])  # Goes to STDIN
        expected_output = str(trial[1])  # Comes from STDOUT

        process = subprocess.Popen(['temp/temp.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)

        stdout, stderr = process.communicate(input_data)

        if not custom_test_function:
            if stdout.strip() != expected_output.strip():
                print("====================================")
                print(f"Test {file_name}#{index} failed")
                print(f"Expected: {expected_output}")
                print(f"Got: {stdout}")
                print("====================================")
                sys.exit(1)
        else:
            if not functiona(stdout.strip(), expected_output):
                print("====================================")
                print(f"Test {file_name}#{index} failed")
                print(f"Expected: {expected_output}")
                print(f"Got: {stdout}")
                print("====================================")
                sys.exit(1)

    print(f"Test {file_name} passed")


for file_name in os.listdir('tests'):
    if file_name.endswith('.psc'):
        file_name = file_name[:-4]
        test_program(file_name)
