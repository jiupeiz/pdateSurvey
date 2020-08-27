#! /usr/bin/python3
import requests
import lxml.html
from tqdm import tqdm
# import csv

def get_keys(id):
    url = "https://repository.library.northeastern.edu/files/" + str(id).strip()
    res = requests.get(url)
    html = lxml.html.fromstring(res.content)
    keys = []
    for elm in html.xpath("//div[@id='metadata']/div/dt"):
        keys.append(elm.text_content().rstrip(':'))
    # metadata_value = []
    # for elm in html.xpath("//div[@id='metadata']/div/dd"):
    #     metadata_value.append(elm.text_content().replace("\n"," " ).strip())
    # record = dict(zip(metadata_scheme, metadata_value))
    # print(record)
    return keys

idFile = open("idlist.txt", "r")
idlist = idFile.readlines()
idFile.close()
keys = []
for id in tqdm(idlist):
    keys = keys + get_keys(id)
with open('keys.txt','a', newline='') as keylist:
    print('Total Metadata Items: ', len(set(keys)))
    for item in list(set(keys)):
        keylist.write(item + "\n")