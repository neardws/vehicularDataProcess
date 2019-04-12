def writeline(line):
    try:
        tclfile = open("gps-bj-am-3x3-test.txt","a")
        tclfile.writelines(line)
    finally:
        if tclfile:
            tclfile.close()


def filter(filename):
    with open(filename) as f:
        content = f.readlines()
    cur_id = 0
    cur_time = 0
    last_x = 0
    last_y = 0
    for line in content:
        l = line.split(' ')
        if cur_id == 0:
            cur_id = int(l[1])
            cur_time = int(l[0])
            last_x = l[2]
            last_y = l[3]
            for time in range(1, cur_time + 1):
                writeline(str(time) + ' ' + str(cur_id) + ' ' + last_x + ' ' + last_y)
        else:
            if int(l[1]) == cur_id:
                last_x = l[2]
                last_y = l[3]
                cur_time = int(l[0])
                writeline(str(cur_time) + ' ' + str(cur_id) + ' ' + last_x + ' ' + last_y)
            else:
                if cur_time == 300:
                    cur_id = int(l[1])
                    cur_time = int(l[0])
                    last_x = l[2]
                    last_y = l[3]
                    for time in range(1, cur_time + 1):
                        writeline(str(time) + ' ' + str(cur_id) + ' ' + last_x + ' ' + last_y)
                else:
                    for time in range(cur_time + 1, 301):
                        writeline(str(time) + ' ' + str(cur_id) + ' ' + last_x + ' ' + last_y)
                    cur_id = int(l[1])
                    cur_time = int(l[0])
                    last_x = l[2]
                    last_y = l[3]
                    for time in range(1, cur_time + 1):
                        writeline(str(time) + ' ' + str(cur_id) + ' ' + last_x + ' ' + last_y)


filter("gps-bj-am-3x3.txt")

