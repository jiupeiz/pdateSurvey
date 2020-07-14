#!/usr/bin/python3

import requests
import lxml.html
import csv

def get_ul(elm):
    ul = []
    for li in elm[1][0]:
        ul.append(li.text_content())
    return ";".join(ul)

def get_title(tt):
    title = []
    for elm in tt[0]:
        title.append(elm.text_content())
    return " ".join(title)

def get_md(format, id):
    url = "https://recorder311.smt.jp/" + format.lower() + "/" + id
    res = requests.get(url)
    html = lxml.html.fromstring(res.content)
    tt = html.xpath("//html/body/div[1]/div/div/div/section[1]/section/section")
    tb = html.xpath("//html/body/div[1]/div/div/div/section[1]/aside[2]/section/dl")
    record = {
        'タイトル' : "%s"%get_title(tt),
        'URL' : url
    }
    scheme = []
    value = []
    for elm in tb:
        key = elm[0].text_content()
        scheme.append(key)
        if key == 'さんかしゃ' or key == 'キーワード':
            value.append(get_ul(elm))
        else:
            value.append(elm[1].text_content())
    
    record.update(dict(zip(scheme, value)))

    return record

if __name__ == '__main__':
    for format in ["Blog", "Movie", "Sound"]:
        idFile = open("idList%s.txt"%format, "r")
        idlist = idFile.readlines()
        idFile.close()
        schemeFile = open("keys.txt", "r")
        keyslist = schemeFile.readlines()
        schemeFile.close()
        template = dict([(key.rstrip("\n"), []) for key in keyslist])
        counter = 1
        rows = []
        for id in idlist:
            formated = {}
            formated.update(template)
            record = get_md(format, id)
            formated.update(record)
            rows.append(formated)
            print("%s: "%format + str(counter) + "/" + str(len(idlist)))
            counter += 1

        with open('md.csv', 'a', newline='') as mdcsv:
            csvWriter = csv.DictWriter(mdcsv, formated.keys())
            csvWriter.writeheader()
            csvWriter.writerows(rows)