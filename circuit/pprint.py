def pformat(circuit):
    indent = 0
    output = []
    line = ''

    skip = 0
    for char in repr(circuit):
        if skip:
            skip -= 1
            continue
        line += char
        if char == '\n':
            output.append(line)
            line = '  ' * indent
        elif char == ',':
            output.append(line)
            line = '\n' + '  ' * indent
            skip = 1
        elif char == '(':
            output.append(line)
            indent += 1
            line = '\n' + '  ' * indent
        elif char == ')':
            output.append(line[:-1])
            indent -= 1
            line = '\n' + '  ' * (indent) + ')'

    assert not indent
    output.append(line.rstrip())
    return ''.join(output)

def pprint(circuit):
    print(pformat(circuit))
