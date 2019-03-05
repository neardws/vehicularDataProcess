import re


def writeline(line):
    try:
        tclfile = open("beijing3pmfilterspeed300node.tcl","a")
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
            if num < 300:
                writeline(line)
            # else:
            #     if num == 480:
            #         for i in range(480,600):
            #             writeline(line.replace(match.group(),'ns_ at '+str(i)))
            #     else:
            #         pass
        else:
            writeline(line)
            # print('not match')


filter("beijing3pmfilterspeed500.tcl")