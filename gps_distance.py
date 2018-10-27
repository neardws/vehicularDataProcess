# -*- coding: UTF-8 -*-

r'''
计算两个GPS点间的距离
@author:Luis1024
@time:2018-06-06 11:00AM

'''

from math import radians, cos, sin, asin, sqrt
import sys
import MySQLdb
import pandas as pd
from datetime import date, datetime, time


reload(sys)
sys.setdefaultencoding('utf-8')

'''
Funciton:从数据库中查找某辆出租的轨迹数据
Input:   None
Output:  以元组类型返回该出租车的轨迹，每条数据以字典形式存储，例如：
        {'GPSLatitude': u'29.516777',
         'GPSLongitude': u'106.554192',
         'GPSTime': datetime.timedelta(0, 10241)
        }
        其中经纬度都是str类型，GPSTime是datetime.timedelta类型，表示的是与这一天2017-03-01 00:00:00的差值，相差0天，10241秒
'''                
def readDB():
    db = MySQLdb.connect(host = "222.198.138.113",user = "lx",passwd = "3124769",db = "Xiong",charset = "utf8")
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT GPSLongitude, GPSLatitude, GPSTime, GPSSpeed, PassengerState FROM Taxi_GPS WHERE VehicleID='渝0100001848';"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception,e:
        print e
    db.close()
    return results
    
'''
Function: 解决GPSTime(datetime.timedelta类型)无法序列化问题，并补上日期2017-03-01
Input：   函数readDB()返回的轨迹数据，元组类型
Output:   轨迹数据，列表类型，其中元素为字典类型，每个元素中GPSTime为datetime类型,GPSLatitude和GPSLongitude为float类型
'''
def GPSTime2Datetime(results_DB):
    basetime = datetime(2017,3,1,0,0,0)
    for i in range(len(results_DB)):
        tmp = results_DB[i]['GPSTime'] #datetimedelta类型
        results_DB[i]['GPSLatitude'] = float(results_DB[i]['GPSLatitude'])  #转为float类型
        results_DB[i]['GPSLongitude'] = float(results_DB[i]['GPSLongitude'])
        results_DB[i]['GPSTime'] = basetime + tmp   #datetime类型
    return list(results_DB)
    
'''
Function: 计算两个GPS点间的距离，采用球面模型
Input：   两个GPS的经纬度
Output:   两个GPS间的距离（米）
'''
def getDistance(lonA, latA, lonB, latB):  #经度1，纬度1，经度2，纬度2
    #ra = 6378140  # radius of equator: meter
    #rb = 6356755  # radius of polar: meter
    r = 6371000    # average radius of the earth: meter
    
    #将十进制度数转化为弧度
    latA, lonA, latB, lonB = map(radians,[latA, lonA, latB, lonB])
    
    # haversine公式
    dlat = latB - latA
    dlon = lonB - lonA
    a = sin(dlat/2)**2 + cos(latA) * cos(latB) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) * r
    return c


def dealVhicle(data):
    """
    Function:
        deal the trajectory of each vehicle, compute the distance betwenn point i-1 and point i
    Args:
        the GPS records 
    Return:
        <Lat, Lon, Time, distance>
    """
    for i in range(len(data)):
        if i == 0:
            data[i]['distance'] = 0
        elif (data[i-1]['GPSLatitude']==data[i]['GPSLatitude']) and (data[i-1]['GPSLongitude']==data[i-1]['GPSLongitude']) :
            data[i]['distance'] = 0
        else:
            data[i]['distance'] = getDistance(data[i-1]['GPSLatitude'], data[i-1]['GPSLongitude'], data[i]['GPSLatitude'], data[i]['GPSLongitude'])
    return data            
            
if __name__ == "__main__":

    result_DB = readDB()
    results = GPSTime2Datetime(result_DB)   
    track1 =pd.DataFrame(dealVhicle(results))
    
    #stay1 = filtered_data3[(filtered_data3.GPSSpeed < 5) & (filtered_data3.distance < 10)]