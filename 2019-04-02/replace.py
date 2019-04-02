import re


def writeline(line):
    try:
        tclfile = open("gps-cd-am-3x3.txt","a")
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
            l = line.replace('$ns_ at ', '').replace(' "$node_(', ' ').replace(') setdest ', ' ').replace(' 0"', '').split(' ')
            writeline(str(int(l[0]) + 1) + ' '+ str(int(l[1]) + 1) + ' ' + l[2] + ' ' + l[3])
        else:
            pass
            # print('not match')


filter("/mnt/d/gps-cd-am-3x3.tcl")

