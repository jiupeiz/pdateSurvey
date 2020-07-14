#!/usr/bin/python3
import requests
import sys
import re

browseUrl = 'https://recorder311.smt.jp/'

def getID(format, pages):
    idList = []
    typeUrl = browseUrl + format + '/page/'
    for page in range(1, int(pages)):
        reqUrl = typeUrl + str(page)
        pattern = re.compile(r'%s/(\d+)/">Read\smore'%format)
        idList.extend(pattern.findall(requests.get(reqUrl).text))
    
    return idList

if __name__ == '__main__':
    # argv ex: blog/movie/sound, number of pages
    idList = getID(sys.argv[1], sys.argv[2])
    for id in idList:
        print(id)