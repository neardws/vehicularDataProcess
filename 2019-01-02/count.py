import re


def count(filename):
    arr = [0]*601
    sum = 0
    i = 0
    max = 0
    maxi = 0
    with open(filename) as f:
        content = f.readlines()
    for line in content:
        print(line)
        pattern = re.compile(r'ns_ at [0-9]\d*')
        match = pattern.search(line)
        if match:
            print(match.group())
            numpattern = re.compile('[0-9]\d*')
            nummatch = numpattern.search(match.group())
            num = int(nummatch.group())
            arr[num] = arr[num] + 1
        else:
            print('not match')
    for times in arr:
        print(times)
        if times > max:
            max = times
            maxi = i
        sum = sum + times
        i = i + 1

    avarage = sum / i
    print('sum is '+ str(sum))
    print('i = ' + str(i))
    print('average is ' + str(avarage))
    print('max is' + str(max))
    print('maxi is '+ str(maxi))

count("beijing3am.tcl")

