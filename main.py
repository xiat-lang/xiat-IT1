import sys

def readf(file):
    with open(file, 'r') as f: return f.read()

def lexer(program):
    i = 0
    tokens = []
    while i < len(program):
        if program[i] == '\"':
            temp = ''
            while i < len(program):
                temp += program[i]
                i += 1
                if program[i] == '"': break
            temp += program[i]
            tokens.append(temp)
        elif program[i].isalnum():
            temp = ''
            while i < len(program):
                if not program[i].isalnum(): break
                temp += program[i]
                i += 1
            i -= 1
            tokens.append(temp)
        elif program[i] == '@':
            while i < len(program):
                i += 1
                if program[i] == '\n': break
        elif not program[i].isspace():
            tokens.append(program[i])
        i += 1
    return tokens
def run(tokens):
    stack = [(len(tokens)-1, '???')] # ??? means end of file basically
    region = {} # name: (codeptr, dataptr)
    # dataptr = {name: value} aka varible
    current = ['???', len(tokens)-1, {}]
    i = 0
    while i < len(tokens): # not to run, only get regions
        if tokens[i] == '.':
            i += 1
            if current[0] != '???':
                region[current[0]] = current[1:]
            current[0] = tokens[i]
            current[1] = i
        i += 1
    region[current[0]] = current[1:]    
    del current
    
    current = 'main'
    i = region['main'][0]
    ptr = '???'
    while i < len(tokens):
        print(region)
        if tokens[i] == 'whome': print('current* ->', current)
        elif tokens[i] == '}': i, current = stack.pop()
        elif tokens[i] == '=':
            varname, value = tokens[i+1], tokens[i+2]
            if ptr != '???':
                region[ptr][1][varname] = value
            else:
                region[current][1][varname] = value
            i += 2
        elif tokens[i] == '*':
            ptr = tokens[i+1]
            i += 1
        elif tokens[i] == 'call':
            stack.append((i, current))
            current, i = tokens[i+1], region[tokens[i+1]][0]
        i += 1
if __name__ == '__main__':
    program = readf(sys.argv[1])
    tokens = lexer(program)
    #for t in tokens: print(t)
    run(tokens)
