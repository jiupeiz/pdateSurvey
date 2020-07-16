#!/usr/bin/python3

import requests
import lxml.html
from tqdm import tqdm

def get_keys(format, id):
    url = "https://recorder311.smt.jp/" + format.lower() + "/" + id
    res = requests.get(url)
    html = lxml.html.fromstring(res.content)
    keys = []

    for elm in html.xpath("//html/body/div[1]/div/div/div/section[1]/aside[2]/section/dl"):
        keys.append(elm[0].text_content())

    return keys

if __name__ == '__main__':
    keys = []
    for format in ["Blog", "Movie", "Sound"]:
        idFile = open("idList%s.txt"%format, "r")
        idlist = idFile.readlines()
        idFile.close()
        print("%s"%format)
        counter = 1
        for id in tqdm(idlist):
            keys.extend(get_keys(format, id))
            # print("%s: "%format + str(counter) + "/" + str(len(idlist)))
            counter += 1
    with open("keys.txt", "a", newline="") as keylist:
        print("Total Metadata Items: ", len(set(keys)))
        for item in list(set(keys)):
            keylist.write(item + "\n")