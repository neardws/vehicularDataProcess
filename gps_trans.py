# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 10:25:59 2017
将原始坐标系转换为百度坐标系
"""

import urllib
import json
import MySQLdb
import sys
import time


db=MySQLdb.connect("127.0.0.1","root","root","od",charset='utf8')
cursor=db.cursor()

def get_gps_origin():
    sql="select id,longtitude,latitude from rfid_original_baidu"
    cursor.execute(sql)
    return cursor.fetchall()
    
def translate_gps(location):
#    mylocation=";".join(location)
    print location
    url="http://api.map.baidu.com/geoconv/v1/?coords=%s&from=3&to=5&ak=rHufFwBkOkOPUUfvamgLdMuG8Ol134hy"
    page=urllib.urlopen(url%location)
    html=page.read()
    data=json.loads(html)
    return data
    
gps_data=get_gps_origin()
result=[]
for temp in gps_data:
    re_temp=translate_gps(str(temp[1])+","+str(temp[2]))["result"][0]
    result.append((re_temp["x"],re_temp["y"],temp[0]))
    
def update_gps(mydata):
    sql="update rfid_original_baidu set longtitude=%s,latitude=%s where id=%s"
    cursor.executemany(sql,mydata)
    db.commit()
    
update_gps(result)