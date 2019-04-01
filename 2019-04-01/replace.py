import re


def writeline(line):
    try:
        tclfile = open("beijing3pm.txt","a")
        tclfile.writelines(line)
    finally:
        if tclfile:
            tclfile.close()


def filter(filename):
    with open(filename) as f:
        content = f.readlines()
    for line in content:
        pattern = re.compile(r'\$ns_ at')
        match = pattern.search(line)
        if match:
            writeline(line.replace('$ns_ at ', '').replace(' "$node_(', ' ')
                      .replace(') setdest ', ' ').replace(' 0"', ''))
        else:
            pass
            # print('not match')

filter("beijing3pmfilterspeed300node.tcl")

