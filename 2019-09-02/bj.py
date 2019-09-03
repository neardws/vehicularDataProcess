import pymysql.cursors
import random
import numpy


def strtonum(str):
    return int(str, 16)


def getx(longitude):
    return strtonum(longitude) - baselongitude


def gety(latitude):
    return strtonum(latitude) - baselatitude


def gettime(timestamp):
    return (strtonum(timestamp) - basetimestamp) / 30

# print(str(gettime('5645c708')))

'''
init node
$node_(0) set X_ 150.0
$node_(0) set Y_ 595.05
$node_(0) set Z_ 0
'''
# def writeinitnode(id, x, y):
#     try:
#         tclfile = open("trace.csv","a")
#         tclfile.writelines(str(x) + " " + str(y) + "\n")
#     finally:
#         if tclfile:
#             tclfile.close()


'''
after init node, node trace
$ns_ at 0.0 "$node_(0) setdest 150.0 595.05 19.96"
'''


def writenodetrace(id, x, y, time):
    try:
        tclfile = open("trace.txt","a")
        tclfile.writelines(str(time)+","+str(id)+","+str(x)+","+str(y)+"\n")
    finally:
        if tclfile:
            tclfile.close()


def write_gps(latitude, longitude):
    try:
        gps_file = open("bj_am_gps.txt", "a")
        gps_file.writelines(str(latitude) + "," + str(longitude) + "\n")
    finally:
        if gps_file:
            gps_file.close()

# timeStamp
# 0
# 2015-11-13 08:30:00 ----> 2015-11-13 08:35:00
# 56452f08  -------> 56453034
# 1447374600
# 1
# 2015-11-13 09:00:00 ----> 2015-11-13 09:05:00
# 56453610  -------> 5645373c
# 1447376400
# 2
# 2015-11-13 22:30:00 ----> 2015-11-13 22:35:00
# 5645f3e8  -------> 5645f514
# ‭1447425000‬
# SQL 查询条件
# Map setup
# 1  3*3km
# latitude 3d05ff longitude b191bb
# 2  5*5km
# latitude 3d0dcf longitude b1998b

'''
Location   AreaSize    Time    VehicleNumber
Beijing      3*3       9AM         252
Beijing      3*3       10PM        193
Beijing      5*5       9AM         377
Beijing      5*5       10PM        284
Chengdu      3*3       9AM
Chengdu      3*3       10PM
'''

baselatitude = 3996231
baselongitude = 11634179
basetimestamp = 1447374600


tablecondition = "WHERE `timeStamp`>='56452f08' AND `timeStamp`<='56453034' " \
          "AND latitude>='3cfa47' AND latitude<='3d05ff'" \
          "AND longitude>='b18603'AND longitude<='b191bb'"


def sqlcreattem():
    sql_creat_tem_table = "CREATE TEMPORARY TABLE tem_table SELECT * FROM vehicleGPS " + tablecondition
    cursor.execute(sql_creat_tem_table)
    print("create tem table success")
    return


condition = " GROUP BY VehicleID"


def sqlcount():
    sql_query_vehicle_id = "SELECT VehicleID, COUNT(*) FROM tem_table " + condition
    cursor.execute(sql_query_vehicle_id)
    return cursor.fetchall()


def getvehicleid():
    vehicleid = []
    sum = 0
    points = sqlcount()
    print("query timelength success")
    for point in points:
        sum += point[1]
    print("SUM is "+str(len(points)))
    avg = sum / len(points)
    print("AVG is "+str(avg))
    i = 0
    num = 3
    for point in points:
        #print(point[1])
        if point[1] >= num:  # value = 24
            i += 1
            vehicleid.append(point[0])
    print("Number behind " + str(num) + " is "+str(i))
    return vehicleid


def get_all_vehicle_id():
    vehicle_id = []
    points = sqlcount()
    for point in points:
        vehicle_id.append(point[0])
    return vehicle_id


def sqlinfo(id):
    sql_query_vehicle_info = "SELECT * FROM tem_table " + "WHERE VehicleID=" + "\'" + id + "\'"
    cursor.execute(sql_query_vehicle_info)
    return cursor.fetchall()


def get_origin_vehicle_number_in_seconds():
    seconds_vehicle_number = {}
    seconds_number = numpy.zeros(300)
    vehicle_id = get_all_vehicle_id()
    for id in vehicle_id:
        infos = sqlinfo(str(id))
        for info in infos:
            # print(str(info))
            time = int(gettime(info[2]))
            seconds_number[time] += 1
    for i in range(300):
        if seconds_number[i] > 0:
            index = str(i)
            seconds_vehicle_number[index] = seconds_number[i]
    return seconds_vehicle_number


def get_process_vehicle_number_in_seconds():
    seconds_vehicle_number= {}
    seconds_number = numpy.zeros(300)
    vehicle_id = getvehicleid()
    for id in vehicle_id:
        infos = sqlinfo(str(id))
        for info in infos:
            # print(str(info))
            x = getx(info[4])
            y = gety(info[3])
            time = int(gettime(info[2]))
            if time == 0:
                # transform x, y into longtude and latitude
                longitude = (x + baselongitude) / 100000
                latitude = (y + baselatitude) / 100000
                write_gps(latitude=latitude, longitude=longitude)
            seconds_number[time] += 1
    for i in range(300):
        if seconds_number[i] > 0:
            index = str(i)
            seconds_vehicle_number[index] = seconds_number[i]
    return seconds_vehicle_number


def getvehicleinfo():
    baseid = 1
    vehicleid = getvehicleid()
    for id in vehicleid:
        infos = sqlinfo(str(id))
        i = 1
        lasttime = 0
        timeid = 0
        lastx = 0
        lasty = 0
        for info in infos:
            print(str(info))
            x = getx(info[4])
            y = gety(info[3])
            time = int(gettime(info[2]))
            if i == 1:
                #writeinitnode(baseid, x, y)
                #writenodetrace(baseid, x, y, time)
                lasttime = time
                timeid = time
                lastx = x
                lasty = y
                i += 1
            else:
                if time == lasttime:
                    # do nothing
                    # remove repeated data
                    pass
                else:
                    # fill data
                    if time - lasttime >= 1:
                        timedifferent = (time - lasttime) * 29
                        addx = (x - lastx) / timedifferent
                        addy = (y - lasty) / timedifferent
                        n = 1
                        while n <= timedifferent:
                            newx = int(lastx + (addx * n))
                            newy = int(lasty + (addy * n))
                            newtime = int(timeid + n)
                            writenodetrace(baseid, newx, newy, newtime)
                            n += 1
                        timeid += timedifferent
                        lasttime = time
                        lastx = x
                        lasty = y
        print("vehicleID" + str(baseid) + "complete")
        baseid += 1


if __name__ == '__main__':
    # 连接数据库
    connect = pymysql.Connect(
        host='120.78.167.211',
        port=3306,
        user='root',
        passwd='King@102321',
        db='vehicleBJ',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()
    print("connect DB success")
    sqlcreattem()
    # print(get_origin_vehicle_number_in_seconds())
    print("*"*32)
    # print(get_process_vehicle_number_in_seconds())
    getvehicleinfo()
