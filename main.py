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
        if tokens[i] == 'whome': 
            if tokens[i+1] == '*':
                print('* ->', ptr)
                i += 1
            else:
                print('current* ->', current)
        elif tokens[i] == '}': i, current = stack.pop()
        elif tokens[i] == '=':
            varname, value = tokens[i+1], tokens[i+2]
            if value == ';': 
                value = '???'  # Default value if not provided
            if ptr != '???':
                region[ptr][1][varname] = value
            else:
                region[current][1][varname] = value
            i += 2

            i += 2
        elif tokens[i] == '#':
            ptr = tokens[i+1]
            i += 1
        elif tokens[i] == 'call':
            stack.append((i, current))  # Save current position and context
            current = tokens[i+1]  # Switch to the new function context
            i = region[current][0]
        elif tokens[i] == 'echo':
            i += 1
            r = ""
            while i < len(tokens):
                if tokens[i] == ';': break
                if tokens[i] == '$':
                    varn = tokens[i+1]
                    r += region[current][1][varn]
                    i += 1
                else:
                    r += tokens[i]
                i += 1
            print(r.replace('"', ''))
        elif tokens[i] == 'read':
            if tokens[i+1] != '$': break
            varname = tokens[i+2]
            value = input('').replace('\r', '')
            if ptr != '???':
                region[ptr][1][varname] = value
            else:
                region[current][1][varname] = value
            i += 2
        i += 1
if __name__ == '__main__':
    program = readf(sys.argv[1])
    tokens = lexer(program)
    #for t in tokens: print(t)
    run(tokens)
