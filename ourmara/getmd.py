#! /usr/bin/python3
import requests
import lxml.html
import csv
from tqdm import tqdm

def get_metadata(id):
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
    url = "https://repository.library.northeastern.edu/files/" + str(id).strip()
    res = requests.get(url)
    html = lxml.html.fromstring(res.content)
    ms = html.xpath("//div[@id='metadata']/div/dt")
    tb = html.xpath("//div[@id='metadata']/div/dd")
    scheme = []
    value = []
    index_range = len(ms)
    index = 0
    for index in range(index_range):
        scheme.append(ms[index].text_content().rstrip(':'))
    for index in range(index_range):
        if ms[index].text_content().rstrip(':') == "Permanent URL":
            value.append(tb[index].text_content())
        else:
            value.append(";".join(tb[index].xpath("text()")).replace("\n      ", " "))
    record = dict(zip(scheme, value))
    # print(record)
    return record

idFile = open("idlist.txt", "r")
idlist = idFile.readlines()
idFile.close()
schemeFile = open("keys.txt", "r")
keylist = schemeFile.readlines()
schemeFile.close()
template = dict([(key.rstrip("\n"), []) for key in keylist])
rows = []
for id in tqdm(idlist):
    formated = {}
    formated.update(template)
    # print(formated)
    record = get_metadata(id)
    formated.update(record)
    # print(formated)
    rows.append(formated)

with open('md.csv', 'a', newline='') as mdcsv:
    csvWriter = csv.DictWriter(mdcsv, formated.keys())
    csvWriter.writeheader()
    csvWriter.writerows(rows)