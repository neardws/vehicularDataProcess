import re


def writeline(line):
    try:
        tclfile = open("chengdu3amfilterspeed.tcl","a")
        tclfile.writelines(line)
    finally:
        if tclfile:
            tclfile.close()


def getspeed(x2, y2, x1, y1, t2, t1):
    return int((abs(x2 - x1) + abs(y2 - y1)) / (t2 - t1))


def gettime(line):
    pattere = re.compile(r'ns_ at [0-9]\d*')
    match = pattere.search(line)
    if match:
        numpattern = re.compile('[0-9]\d*')
        nummatch = numpattern.search(match.group())
        time = nummatch.group()
        return int(time)
    else:
        return -666


def getxy(line):
    pattere = re.compile(r'setdest [0-9]\d* [0-9]\d*')
    match = pattere.search(line)
    if match:
        numpattern = re.compile('[0-9]\d*')
        nummatch = numpattern.findall(match.group())
        y = nummatch.pop()
        x = nummatch.pop()
        xy = list()
        xy.append(y)
        xy.append(x)
        return xy
    else:
        return -666


class Node:
    def __init__(self, id, speed):
        self.id = id
        self.speed = speed
    def __repr__(self):
        return repr((self.id, self.speed))


def speedset(filename):
    with open(filename) as f:
        content = f.readlines()
    id = -666
    nodelist = list()
    for line in content:
        xy = getxy(line)
        if xy == -666:
            pass
        else:
            pattern = re.compile(r'node_\([0-9]\d*')
            match = pattern.search(line)
            if match:
                idpattern = re.compile('[0-9]\d*')
                idmatch = idpattern.search(match.group())
                idnum = int(idmatch.group())
                if id == -666:
                    id = idnum
                    # print(id)
                    # print(node.id)
                    xy1 = getxy(line)
                    time1 = gettime(line)
                else:
                    if id == idnum:
                        xy2 = getxy(line)
                        time2 = gettime(line)
                        # print("idnum = "+ str(idnum))
                    else:
                        if time2 == time1:
                            # print("time2 = time1")
                            pass
                        else:
                            x2 = xy2.pop()
                            y2 = xy2.pop()
                            x1 = xy1.pop()
                            y1 = xy1.pop()
                            # print("x2 =" + x2 + " y2 =" + y2 + " x1 =" + x1 + " y1 =" + y1 + " time2 =" + str(time2) + " time1 =" + str(time1))
                            speed = getspeed(int(x2), int(y2), int(x1), int(y1), time2, time1)
                            nodelist.append(Node(id, speed))
                            id = idnum
                            time1 = gettime(line)
                            xy1 = getxy(line)
    print(nodelist)
    sortlist = sorted(nodelist, key=lambda node: node.speed, reverse=True)
    speedset = set()
    print(sortlist)
    num = 500
    for node in sortlist:
        speedset.add(node.id)
        print(node)
        if len(speedset) == num:
            break
    print(speedset)
    return speedset


def filter(filename):
    idset = speedset(filename)
    print(idset)
    with open(filename) as f:
        content = f.readlines()
    i = 0
    number = -123
    for line in content:
        # print(line)
        pattern = re.compile(r'node_\([0-9]\d*')
        match = pattern.search(line)
        if match:
            # print(match.group())
            numpattern = re.compile('[0-9]\d*')
            nummatch = numpattern.search(match.group())
            num = int(nummatch.group())
            if num in idset:
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
            pass
            # print('not match')


filter("chengdu3am.tcl")

