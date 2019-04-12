def writeline(line):
    try:
        tclfile = open("gps-bj-am-3x3-test.txt","a")
        tclfile.writelines(line)
    finally:
        if tclfile:
            tclfile.close()


def filter(filename):
    for t in range(122,300):
        writeline('\n' + str(t) + ' 500 2769 2376')


filter("gps-bj-am-3x3-test.txt")

