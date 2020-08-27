#!/usr/bin/python3

import csv
from tqdm import tqdm

def splt_kw(kwList):
    kws = kwList.split(";")
    for kw in kws:
        print(kw)
    return 0

if __name__ == '__main__':
    with open("md.csv", "r") as csvFile:
        csvObj = csv.reader(csvFile)
        kwll = list(csvObj)
        for kwl in kwll:
            splt_kw(kwl[0])
