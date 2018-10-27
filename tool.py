baselatitude = 3996231
baselongitude = 11634179
basetimestamp = 1447411712


def strtonum(str):
    return int(str, 16)


def getx(longitude):
    return strtonum(longitude) - baselongitude


def gety(latitude):
    return strtonum(latitude) - baselatitude


def gettime(timestamp):
    return (strtonum(timestamp) - basetimestamp) / 30

# print(str(gettime('5645c708')))


def writedoc():
    
