import re


def writeline(line):
    try:
        tclfile = open("beijing3pmfilterspeed500addnode.tcl","a")
        tclfile.writelines(line)
    finally:

        if tclfile:
            tclfile.close()


def filter(filename):
    with open(filename) as f:
        content = f.readlines()
    i = 0
    for line in content:
        # print(line)
        pattern = re.compile(r'ns_ at [0-9]\d*')
        match = pattern.search(line)
        if match:
            numpattern = re.compile('[0-9]\d*')
            nummatch = numpattern.search(match.group())
            num = int(nummatch.group())
            if num < 480:
                writeline(line)
            else:
                if num == 480:
                    for i in range(491,600):
                        writeline(line.replace(match,'ns_ at '+str(i)))
                else:
                    pass
        else:
            writeline(line)
            # print('not match')


filter("beijing3pmfilterspeed500.tcl")