import pymysql.cursors
import random
import numpy


def strtonum(str):
    return int(str, 16)


def getx(longitude):
    return strtonum(longitude) - baselongitude


def gety(latitude):
    return strtonum(latitude) - baselatitude


def get_time(timestamp):
    return strtonum(timestamp) - basetimestamp

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
        tclfile = open("bj_am_trace.txt","a")
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
            time = int(get_time(info[2]))
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
            time = int(get_time(info[2]))
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


def get_vehicle_info():
    base_id = 1
    vehicle_id = getvehicleid()
    process_vehicle_number = {}
    vehicle_number = numpy.zeros(301)
    end_vehicle_number = 0
    begin_vehicle_number = 0
    for id in vehicle_id:
        infos = sqlinfo(str(id))
        last_time = 0
        last_x = 0
        last_y = 0
        info_number = 0
        for info in infos:
            info_number += 1
            print(str(info))
            x = getx(info[4])
            y = gety(info[3])
            time = int(get_time(info[2])) + 1
            if info_number == 1:
                if time <= 30:
                    begin_vehicle_number += 1
                    for j in range(time):
                        writenodetrace(base_id, x, y, j + 1)
                        vehicle_number[j] += 1
                    longitude = (x + baselongitude) / 100000
                    latitude = (y + baselatitude) / 100000
                    write_gps(latitude=latitude, longitude=longitude)
                else:
                    writenodetrace(base_id, x, y, time)
                last_time = time
                last_x = x
                last_y = y
            else:
                time_different = time - last_time
                if time_different >= 1:
                    add_x = (x - last_x) / time_different
                    add_y = (y - last_y) / time_different
                    n = 1
                    while n <= time_different:
                        new_x = int(last_x + (add_x * n))
                        new_y = int(last_y + (add_y * n))
                        new_time = int(last_time + n)
                        if new_time <= 300:
                            writenodetrace(base_id, new_x, new_y, new_time)
                            vehicle_number[new_time] += 1
                        n += 1
                    last_time = time
                    last_x = x
                    last_y = y
        # process last info
        last_info = infos[-1]
        x = getx(last_info[4])
        y = gety(last_info[3])
        time = int(get_time(last_info[2])) + 1
        if time >= 270:
            if time < 300:
                end_vehicle_number += 1
                for end_time in range(time+1, 301):
                    print("%"*32)
                    print(end_time)
                    writenodetrace(base_id, x, y, end_time)
                    vehicle_number[end_time] += 1
        print("vehicleID" + str(base_id) + "complete")
        base_id += 1
    print("#"*64)
    print("begin number is" + str(begin_vehicle_number))
    print("end number is" + str(end_vehicle_number))
    for i in range(300):
        process_vehicle_number[str(i)] = vehicle_number[i]
    return process_vehicle_number


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
    print(get_vehicle_info())
