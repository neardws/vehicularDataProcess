import pymysql.cursors

baseid = 0

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

# SQL 查询条件
condition = "WHERE `timeStamp`>='5645c000' AND `timeStamp`<='5645c708' " \
          "AND latitude>='3cfa47' AND latitude<='3d052e'" \
          "AND longitude>='b18603'AND longitude<='b1954a' GROUP BY VehicleID"


def getvehicleid():
    sql_query_vehicle_id = "SELECT COUNT(*) FROM vehicleGPS " + condition
    cursor.execute(sql_query_vehicle_id)
    return cursor.fetchall()


def timelength():
    sum = 0
    times = getvehicleid()
    print("query timelength success")
    for time in times:
        sum += time[0]
        print(str(time[0]))
    print("SUM is "+str(len(times)))
    avg = sum / len(times)
    print("AVG is "+str(avg))
    i = 0
    for time in times:
        if time[0] >= avg:
            i += 1
    print("Number behind AVG is "+str(i))


timelength()
