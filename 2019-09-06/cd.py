import math
import numpy
import pymysql.cursors

# 连接数据库
connect = pymysql.Connect(
    host='120.78.167.211',
    port=3306,
    user='root',
    passwd='King@102321',
    db='vehicleCD',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()
print("connect DB success")


# def writeinitnode(id, x, y):
#     try:
#         tclfile = open("chengdu.txt","a")
#         tclfile.writelines("$node_("+str(id)+") set X_ "+str(x)+"\n")
#         tclfile.writelines("$node_("+str(id)+") set Y_ "+str(y)+"\n")
#         tclfile.writelines("$node_("+str(id)+") set Z_ "+str(0)+"\n")
#     finally:
#         if tclfile:
#             tclfile.close()


'''
after init node, node trace
$ns_ at 0.0 "$node_(0) setdest 150.0 595.05 19.96"
'''


def writenodetrace(id, x, y, time):
    try:
        tclfile = open("cd_am_trace.txt","a")
        tclfile.writelines(str(time)+","+str(id)+","+str(x)+","+str(y)+"\n")
    finally:
        if tclfile:
            tclfile.close()


def write_gps(latitude, longitude):
    try:
        gps_file = open("cd_am_gps.txt", "a")
        gps_file.writelines(str(latitude) + "," + str(longitude) + "\n")
    finally:
        if gps_file:
            gps_file.close()


# time setup
# 1 9AM
# 2014/8/20 9:00 AM ----> 9:30 AM
#
# map setup
# 1.5 x 1.5 KM
# 中国四川省成都市青羊区文庙前街75号
# 30.6572218073,104.0655900989
# latitude    30.657221   -----------> 30.672221
# longitude   104.065590  -----------> 104.080590
#

# SELECT
# 	*
# FROM
# 	`VehicleGPS`
# WHERE
# 	`timeStamp` >= '2014-08-20 09:00:00'
# 	AND `timeStamp` <= '2014-08-20 09:30:00'
# 	AND latitude >= 30.646166
# 	AND latitude <= 30.676166
# 	AND longitude >= 104.045824
# 	AND longitude <= 104.075824

tablecondition = "WHERE `timeStamp`>='2014-08-20 09:00:00' " \
                 "AND `timeStamp`<='2014-08-20 09:05:00' " \
          "AND latitude>=30.657221 AND latitude<=30.672221" \
          "AND longitude>=104.065590 AND longitude<=104.080590"


def sqlcreattem():
    sql_creat_tem_table = "CREATE TEMPORARY TABLE tem_table SELECT * FROM VehicleGPS " + tablecondition
    cursor.execute(sql_creat_tem_table)
    print("create tem table success")
    return


condition = " GROUP BY VehicleID"


def sqlcount():
    sql_query_vehicle_id = "SELECT VehicleID, COUNT(*) FROM tem_table " + condition
    cursor.execute(sql_query_vehicle_id)
    return cursor.fetchall()


def get_vehicle_id():
    vehicle_id = []
    sum = 0
    # point[0] VehicleID
    # point[1] COUNT(*)
    points = sqlcount()
    print("query timelength success")
    for point in points:
        sum += point[1]
    print("SUM is "+str(len(points)))
    avg = sum / len(points)
    print("AVG is "+str(avg))
    i = 0
    num = 8
    for point in points:
        if point[1] >= num:  # value = 24
            i += 1
            vehicle_id.append(point[0])
    print("Number behind " + str(num) + " is "+str(i))
    return vehicle_id


def sqlinfo(id):
    sql_query_vehicle_info = "SELECT latitude, longitude, " \
                             "TIMESTAMPDIFF(SECOND, '2014-08-20 09:00:00', timeStamp) FROM tem_table " \
                             + "WHERE VehicleID = " + str(id) + " ORDER BY timeStamp ASC"
    cursor.execute(sql_query_vehicle_info)
    return cursor.fetchall()

baselatitude = 3065722.1
baselongitude = 10406559.0

def get_x(x):
    return int(x * 100000 - baselongitude)


def get_y(y):
    return int(y * 100000 - baselatitude)


# timestamp in mysql = 1s
# / depend on timestamp which we want
def get_time(time):
    return math.floor(int(time / 1))


def get_vehicle_info():
    base_id = 1
    vehicle_id = get_vehicle_id()
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
            x = get_x(info[1])
            y = get_y(info[0])
            time = int(get_time(info[2])) + 1
            if info_number == 1:
                if time <= 30:
                    begin_vehicle_number += 1
                    for j in range(time):
                        writenodetrace(base_id, x, y, j + 1)
                        vehicle_number[j] += 1
                    write_gps(latitude=info[0], longitude=info[1])
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
        x = get_x(last_info[1])
        y = get_y(last_info[0])
        time = int(get_time(last_info[2])) + 1
        if time >= 270:
            if time < 300:
                end_vehicle_number += 1
                for end_time in range(time + 1, 301):
                    print("%" * 32)
                    print(end_time)
                    writenodetrace(base_id, x, y, end_time)
                    vehicle_number[end_time] += 1
        print("vehicleID" + str(base_id) + "complete")
        base_id += 1
    print("#" * 64)
    print("begin number is" + str(begin_vehicle_number))
    print("end number is" + str(end_vehicle_number))
    for i in range(300):
        process_vehicle_number[str(i)] = vehicle_number[i]
    return process_vehicle_number


if __name__ == '__main__':
    sqlcreattem()
    print(get_vehicle_info())
