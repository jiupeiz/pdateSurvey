import requests
import lxml.html
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
counter = 1
keys = []
for id in idlist:
    keys = keys + get_keys(id)
    print(str(counter) + '/' + str(len(idlist)))
    counter += 1
with open('keys.txt','a', newline='') as keylist:
    print('Total Metadata Items: ', len(set(keys)))
    for item in list(set(keys)):
        keylist.write(item + "\n")