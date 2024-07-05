import os


def test(a, x):
    data = None
    with open('FileB.txt', 'r') as f:
        data = f.read()
    # delete the file
    os.remove('FileB.txt')
    return data == x
