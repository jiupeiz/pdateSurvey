import requests
import lxml.html
import csv

def get_metadata(id):
    url = "https://repository.library.northeastern.edu/files/" + str(id).strip()
    res = requests.get(url)
    html = lxml.html.fromstring(res.content)
    metadata_scheme = []
    for elm in html.xpath("//div[@id='metadata']/div/dt"):
        metadata_scheme.append(elm.text_content().rstrip(':'))
    metadata_value = []
    for elm in html.xpath("//div[@id='metadata']/div/dd"):
        metadata_value.append(elm.text_content().replace("\n"," " ).strip())
    record = dict(zip(metadata_scheme, metadata_value))
    print(record)
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
        csvWriter = csv.DictWriter(mdcsv, record.keys())
        csvWriter.writeheader()
        csvWriter.writerow(record)
