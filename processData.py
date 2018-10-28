import pymysql.cursors

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

baselatitude = 3996231
baselongitude = 11634179
basetimestamp = 1447425000


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


def writeinitnode(id, x, y):
    try:
        tclfile = open("output2.tcl","a")
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
        tclfile = open("output2.tcl","a")
        tclfile.writelines("$ns_ at "+str(time)+" \"$node_("+str(id)+") setdest "+str(x)+" "+str(y)+" "+str(0)+"\"\n")
    finally:
        if tclfile:
            tclfile.close()

# timeStamp
# 1
# 2015-11-13 09:00:00 ----> 2015-11-13 09:00:00
# 56453610  -------> 56453D18
# >=22 428vehicles
# >=24 378vehicles
# 2
# 2015-11-13 22:30:00 ----> 2015-11-13 23:00:00
# 5645F3E8  -------> 5645FAF0
# >=22 234vehicles
# >=24 217vehicles
# SQL 查询条件


condition = "WHERE `timeStamp`>='5645f3e8' AND `timeStamp`<='5645faf0' " \
          "AND latitude>='3cfa47' AND latitude<='3d052e'" \
          "AND longitude>='b18603'AND longitude<='b1954a' GROUP BY VehicleID"


def sqlcount():
    sql_query_vehicle_id = "SELECT VehicleID, COUNT(*) FROM vehicleGPS " + condition
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
        if point[1] >= 24:  # value = 24
            i += 1
            vehicleid.append(point[0])
    print("Number behind AVG is "+str(i))
    return vehicleid


infocondition = "WHERE `timeStamp`>='5645f3e8' AND `timeStamp`<='5645faf0' " \
          "AND latitude>='3cfa47' AND latitude<='3d052e'" \
          "AND longitude>='b18603'AND longitude<='b1954a'"


def sqlinfo(id):
    sql_query_vehicle_info = "SELECT * FROM vehicleGPS " + infocondition + " AND VehicleID=" + "\'" + id + "\'"
    cursor.execute(sql_query_vehicle_info)
    return cursor.fetchall()


def getvehicleinfo():
    baseid = 0
    vehicleid = getvehicleid()
    for id in vehicleid:
        infos = sqlinfo(str(id))
        i = 1
        for info in infos:
            print(str(info))
            x = getx(info[4])
            y = gety(info[3])
            time = int(gettime(info[2]))
            if i == 1:
                writeinitnode(baseid, x, y)
                writenodetrace(baseid, x, y, time)
                i += 1
            else:
                writenodetrace(baseid, x, y, time)
        print("vehicleID" + str(baseid) + "complete")
        baseid += 1


getvehicleinfo()
