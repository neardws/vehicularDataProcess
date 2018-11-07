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


def writeinitnode(id, x, y):
    try:
        tclfile = open("chengdu3am.tcl","a")
        tclfile.writelines("$node_("+str(id)+") set X_ "+str(x)+"\n")
        tclfile.writelines("$node_("+str(id)+") set Y_ "+str(y)+"\n")
        tclfile.writelines("$node_("+str(id)+") set Z_ "+str(0)+"\n")
    finally:
        if tclfile:
            tclfile.close()


'''
after init node, node trace
$ns_ at 0.0 "$node_(0) setdest 150.0 595.05 19.96"
'''


def writenodetrace(id, x, y, time):
    try:
        tclfile = open("chengdu3am.tcl","a")
        tclfile.writelines("$ns_ at "+str(time)+" \"$node_("+str(id)+") setdest "+str(x)+" "+str(y)+" "+str(0)+"\"\n")
    finally:
        if tclfile:
            tclfile.close()


# time setup
# 1 9AM
# 2014/8/20 9:00 AM ----> 9:30 AM
# 2 10PM
# 2014/8/20 10:30 PM -----> 11:00 PM
#
# map setup
# 1 3 x 3 KM
# 中国四川省成都市武侯区武侯祠横街2号
# latitude    30.646166   -----------> 30.676166
# longitude   104.045824  -----------> 104.075824
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
                 "AND `timeStamp`<='2014-08-20 09:30:00' " \
          "AND latitude>=30.646166 AND latitude<=30.676166" \
          "AND longitude>=104.045824 AND longitude<=104.075824"


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
    points = sqlcount()
    print("query timelength success")
    for point in points:
        sum += point[1]
    print("SUM is "+str(len(points)))
    avg = sum / len(points)
    print("AVG is "+str(avg))
    i = 0
    for point in points:
        if point[1] >= 28:  # value = 24
            i += 1
            vehicleid.append(point[0])
    print("Number behind AVG is "+str(i))
    return vehicleid


def sqlinfo(id):
    sql_query_vehicle_info = "SELECT VehicleID, latitude, longitude, " \
                             "TIMESTAMPDIFF(SECOND, '2014-08-20 09:00:00') FROM tem_table " \
                             + "WHERE VehicleID=" + str(id)
    cursor.execute(sql_query_vehicle_info)
    return cursor.fetchall()


def getvehicleinfo():
    baseid = 0
    vehicleid = getvehicleid()
    for id in vehicleid:
        infos = sqlinfo(id)
        i = 1
        lasttime = 0
        timeid = 0
        lastx = 0
        lasty = 0
        for info in infos:
            print(str(info))
            x = getx(info[2])
            y = gety(info[1])
            time = gettime(info[3])
            if i == 1:
                writeinitnode(baseid, x, y)
                writenodetrace(baseid, x, y, time)
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
                        timedifferent = (time - lasttime) * 2
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


baselatitude = 3064616.6
baselongtitude = 10404582.4


def getx(x):
    return int(x * 100000 - baselongtitude)


def gety(y):
    return int(y * 100000 - baselatitude)


def gettime(time):
    return int(time / 15)
