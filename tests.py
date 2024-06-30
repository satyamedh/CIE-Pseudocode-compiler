import os
import importlib
import subprocess
import json


def test_program(file_name):
    try:
        solutions = json.load(open(f'tests/solutions/{file_name}.json'))
    except FileNotFoundError:
        print(f"No solutions found for {file_name}")
        return

    # the solutions are stored in the trials variable
    # each trial is a list of inputs and expected outputs

    # run the main.py file with the input
    # os.system(f'python main.py tests/{file_name}.psc -o temp/temp -c temp/temp.c')
    compiler_process = subprocess.Popen(['python', 'main.py', f'tests/{file_name}.psc', '-o', 'temp/temp', '-c',
                                         'temp/temp.c'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = compiler_process.communicate()
    if stderr:
        print("====================================")
        print(f"Compilation might've failed for {file_name}")
        print(stderr)
        print("====================================")
        return

    for index, trial in enumerate(solutions['trials']):
        input_data = str(trial[0])  # Goes to STDIN
        expected_output = str(trial[1])  # Comes from STDOUT

        process = subprocess.Popen(['temp/temp.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)

        stdout, stderr = process.communicate(input_data)

        if stdout.strip() != expected_output.strip():
            print("====================================")
            print(f"Test {file_name}#{index} failed")
            print(f"Expected: {expected_output}")
            print(f"Got: {stdout}")
            print("====================================")
            return

    print(f"Test {file_name} passed")


for file_name in os.listdir('tests'):
    if file_name.endswith('.psc'):
        file_name = file_name[:-4]
        test_program(file_name)
