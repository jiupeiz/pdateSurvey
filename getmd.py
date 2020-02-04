import requests
import lxml.html
import csv

def get_metadata(id):
    url = "https://repository.library.northeastern.edu/files/" + str(id).strip()
    res = requests.get(url)
    html = lxml.html.fromstring(res.content)
    metadata = html.xpath("//div[@id='metadata']/div/dd")
    record =[]
    record.append(id)
    for elms in metadata:
        record.append(elms.text_content())
    return record

idFile = open("idlist.txt", "r")
idlist = idFile.readlines()
idFile.close()
counter = 1
for id in idlist:
    record = get_metadata(id)
    print(str(counter) + '/' + str(len(idlist)))
    counter += 1
    with open('md.csv','a', newline='') as mdcsv:
        csvWriter = csv.writer(mdcsv)
        csvWriter.writerow(record)
