#!/usr/bin/python3

import csv
import os

def compute():
    path = "/Users/fanyinyi/Downloads/data/"
    flist = os.listdir(path)
    for i in flist:

        if i.endswith(".tsv"):
            #print(i[0:4]+'-'+i[5:7])
            with open(path+i) as tsv_file:
            #with open("/Users/fanyinyi/Downloads/data/test2.tsv") as tsv_file:

                reader = csv.reader(tsv_file.read().splitlines(), delimiter='\t')
                #reader = csv.reader(tsv_file.read().splitlines())
                lists=[]
                for k,row in enumerate(reader):
                    print len(row)
                    if(len(row))>5:
                        message_info = {
                            'n': row[2],
                            'prev_title': row[3],
                            'curr_title': row[4],
                            'date': i[0:4]+'-'+i[5:7]
                        }
                    if(len(row))<5:
                        message_info = {
                            'n': row[3],
                            'prev_title': row[0],
                            'curr_title': row[1],
                            'date': i[0:4]+'-'+i[5:7]
                        }
                    lists.append(message_info)
                    print(lists)
                    if (k >= 0):
                        break
if __name__ == '__main__':
    compute()