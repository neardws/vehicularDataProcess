import math

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
        tclfile = open("chengdu.txt","a")
        tclfile.writelines(str(id)+" "+str(time)+" "+str(x)+" "+str(y)+"\n")
    finally:
        if tclfile:
            tclfile.close()


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


def getvehicleid():
    vehicleid = []
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
    num = 18
    for point in points:
        if point[1] >= num:  # value = 24
            i += 1
            if i <= 110:
                vehicleid.append(point[0])
    print("Number behind " + str(num) + " is "+str(i))
    return vehicleid


def sqlinfo(id):
    sql_query_vehicle_info = "SELECT latitude, longitude, " \
                             "TIMESTAMPDIFF(SECOND, '2014-08-20 09:00:00', timeStamp) FROM tem_table " \
                             + "WHERE VehicleID = " + str(id) + " ORDER BY timeStamp ASC"
    cursor.execute(sql_query_vehicle_info)
    return cursor.fetchall()


def getvehicleinfo():
    baseid = 1
    vehicleid = getvehicleid()
    for id in vehicleid:
        infos = sqlinfo(id)
        i = 1
        lasttime = 0
        lastx = 0
        lasty = 0
        # First node could be any time
        for info in infos:
            # print(str(info))
            x = getx(info[1])
            y = gety(info[0])
            time = gettime(info[2])
            print("(" + str(x) + "," + str(y) + "," + str(time) + ")")
            if i == 1:
                #writeinitnode(baseid, x, y)
                writenodetrace(baseid, x, y, time)
                lasttime = time
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
                        timedifferent = time - lasttime
                        addx = (x - lastx) / timedifferent
                        addy = (y - lasty) / timedifferent
                        n = 1
                        while n <= timedifferent:
                            newx = int(lastx + (addx * n))
                            newy = int(lasty + (addy * n))
                            newtime = int(lasttime + n)
                            writenodetrace(baseid, newx, newy, newtime)
                            n += 1
                        lasttime = time
                        lastx = x
                        lasty = y
        print("vehicleID" + str(baseid) + "complete")
        baseid += 1


baselatitude = 3065722.1
baselongtitude = 10406559.0


def getx(x):
    return int(x * 100000 - baselongtitude)


def gety(y):
    return int(y * 100000 - baselatitude)


# timestamp in mysql = 1s
# / depend on timestamp which we want
def gettime(time):
    return math.floor(int(time / 1))



sqlcreattem()
getvehicleinfo()

#getvehicleid()
