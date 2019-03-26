import re


def writeline(line):
    try:
        tclfile = open("beijing3pmfilterspeed500.tcl","a")
        tclfile.writelines(line)
    finally:

        if tclfile:
            tclfile.close()


def getspeed(x2, y2, x1, y1, t2, t1):
    return int((abs(x2 - x1) + abs(y2 - y1)))


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
    def __init__(self, id, speed, times):
        self.id = id
        self.speed = speed
        self.times = times
    def __repr__(self):
        return repr((self.id, self.speed, self.times))


def speedset(filename):
    with open(filename) as f:
        content = f.readlines()
    id = -666
    nodelist = list()
    for line in content:
        xy = getxy(line)
        if xy == -666:
            # print("pass")
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
                    times = 0
                    # print("id = -666")
                else:
                    if id == idnum:
                        xy2 = getxy(line)
                        time2 = gettime(line)
                        times = times + 1
                        # print("id = idnum")
                        # print("idnum = "+ str(idnum))
                    else:
                        if time2 == time1:
                            # print("time2 = time1")
                            pass
                        else:
                            # print(xy2)
                            # print(id)
                            if len(xy2):
                                x2 = xy2.pop()
                                y2 = xy2.pop()
                                x1 = xy1.pop()
                                y1 = xy1.pop()
                                # print("x2 =" + x2 + " y2 =" + y2 + " x1 =" + x1 + " y1 =" + y1 + " time2 =" + str(time2) + " time1 =" + str(time1))
                                speed = getspeed(int(x2), int(y2), int(x1), int(y1), time2, time1)
                                nodelist.append(Node(id, speed, times))
                                id = idnum
                                time1 = gettime(line)
                                xy1 = getxy(line)
                            else:
                                print(str(id) + "list is empty")
                                id = -666
    print(nodelist)
    sortlist = sorted(nodelist, key=lambda node: node.speed, reverse=True)
    speedset = set()
    print(sortlist)
    num = 500
    for node in sortlist:
        speedset.add(node.id)
        # print(node)
        if len(speedset) == num:
            break
    # sortlistTime = sorted(nodelist, key=lambda node: node.times, reverse=True)
    # for node in sortlistTime:
    #     if node.id not in speedset:
    #         speedset.add(node.id)
    #         print(node)
    #     if len(speedset) == 500:
    #         break
    print(speedset)
    return speedset


# def filter(filename):
#     idset = speedset(filename)
#     print(idset)
#     with open(filename) as f:
#         content = f.readlines()
#     i = 0
#     number = -123
#     for line in content:
#         # print(line)
#         pattern = re.compile(r'node_\([0-9]\d*')
#         match = pattern.search(line)
#         if match:
#             # print(match.group())
#             numpattern = re.compile('[0-9]\d*')
#             nummatch = numpattern.search(match.group())
#             num = int(nummatch.group())
#             if num in idset:
#                 atpattern = re.compile(r'at [0-9]\d*')
#                 atmatch = atpattern.search(line)
#                 if atmatch:
#                     atnumpattern = re.compile('[0-9]\d*')
#                     atnummatch = atnumpattern.search(atmatch.group())
#                     atnum = int(atnummatch.group())
#                     if atnum <= 600:
#                         if number == -123:
#                             writeline(line.replace(match.group(), 'node_(' + str(i)))
#                             number = num
#                         else:
#                             if number == num:
#                                 writeline(line.replace(match.group(), 'node_(' + str(i)))
#                             else:
#                                 i = i + 1
#                                 number = num
#                                 writeline(line.replace(match.group(), 'node_(' + str(i)))
#         else:
#             pass
#             # print('not match')

def filter(filename):
    idset = speedset(filename)
    # print(idset)
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


filter("beijing3pm.tcl")

