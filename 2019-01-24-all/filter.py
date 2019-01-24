import random
import re


def writeline(line):
    try:
        tclfile = open("chengdu3amfilter2.tcl","a")
        tclfile.writelines(line)
    finally:
        if tclfile:
            tclfile.close()


def roandmeset(num, size):
    i = 0
    randomset = set()
    for i in range(0,size):
        randomnum = random.randint(0, num)
        if randomnum in randomset:
            pass
        else:
            randomset.add(random.randint(0, num))
            i = i + 1
    print("i =" + str(i))
    return randomset


def filter(filename):
    with open(filename) as f:
        content = f.readlines()
    set = roandmeset(2263, 250)
    print("set is"+ str(set))
    i = 0
    number = -123
    for line in content:
        print(line)
        pattern = re.compile(r'node_\([0-9]\d*')
        match = pattern.search(line)
        if match:
            print(match.group())
            numpattern = re.compile('[0-9]\d*')
            nummatch = numpattern.search(match.group())
            num = int(nummatch.group())
            if num in set:
                if number == -123:
                    writeline(line.replace(match.group(), 'node_(' + str(i)))
                    number = num
                else:
                    if number == num:
                        writeline(line.replace(match.group(), 'node_(' + str(i)))
                    else:
                        i = i + 1
                        number = num
                        writeline(line.replace(match.group(), 'node_(' + str(i)))
        else:
            print('not match')


filter("chengdu3am.tcl")

