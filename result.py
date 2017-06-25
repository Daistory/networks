#!usr/bin/python
# -*-coding:utf-8-*-

import os
import csv
dir_str = "result"
titl_list = ['NetID']
for i in range(500):
    titl_list.append('nodeID'+str(i+1))
out = open('result.csv', 'w')
csv_writer = csv.writer(out)
csv_writer.writerow(titl_list)
out.close()
for root, dirs, file_name_list in os.walk(dir_str):
    for file_name in file_name_list:
        fr = open(dir_str+"/"+file_name, 'r').read()
        with open('result.csv', 'a') as f:
            f.write(fr)
