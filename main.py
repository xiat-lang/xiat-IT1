import sys

def readf(file):
    with open(file, 'r') as f: return f.read()

if __name__ == '__main__':
    program = readf(sys.argv[1])
    print(program)
