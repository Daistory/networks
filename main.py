#!usr/bin/python
# -*-coding:utf-8-*-
import method
import os

relative_path = "result/"
for root, dirs, file_name_list in os.walk("data"):
    print file_name_list
file_name = file_name_list[5]
graph = method.getGraph("data/" + file_name)
print "Create a graph"
amt_vaccination = graph.number_of_nodes()
print amt_vaccination
point_list = method.getRankByCluDe(graph, amt_vaccination)
print "Get a vaccination list"
print len(point_list)
method.saveData(point_list, relative_path + file_name)
print "Save the result"
print "Finish"
# for file_name in file_name_list:
#     graph = method.getGraph("data/" + file_name)
#     print "Create a graph"
#     amt_vaccination = graph.number_of_nodes()
#     print amt_vaccination
#     point_list = method.getRandWalkByRadius(graph, amt_vaccination, amt_vaccination / 5000)
#     print "Get a vaccination list"
#     # print len(point_list)
#     method.saveData(point_list, relative_path + file_name)
#     print "Save the result"
# print "Finish"
