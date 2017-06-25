# -*- coding:utf-8 -*-
import csv
import gc
import networkx as nx
from numpy import double
from numpy import random


def saveData(list, file_name):
    """
    :param list: 需要保存的list
    :param file_name: 需要保存的相对位置
    :return:
    """
    print len
    temp_list = []
    temp_list.append(file_name[7:-4])
    out = open(file_name, 'w')
    csv_writer = csv.writer(out)
    index = len(list) / 500
    if index * 500 < len(list):
        index += 1
    print index
    for i in range(index - 1):
        csv_writer.writerow(temp_list + list[i * 500:(i + 1) * 500])
    csv_writer.writerow(temp_list + list[(index - 1) * 500:])
    out.close()


def getGraph(file_name):
    csv_reader = csv.reader(open(file_name))
    graph = nx.Graph()
    for temp_list in csv_reader:
        temp_list = map(int, temp_list)
        graph.add_edge(temp_list[0], temp_list[1])
    return graph


def getCenPoint(graph, amt_vaccination):
    """
    寻找网络中介数中心性最大的部分点
    :param graph: 无向图
    :param amt_vaccination: 需要免疫的节点的数量
    :return: 返回amt_vaccination大小的list，里面代表对应需要免疫的节点
    """
    all_centrality_dic = nx.betweenness_centrality(graph)
    all_centrality_dic = sorted(all_centrality_dic.iteritems(), key=lambda asd: asd[1], reverse=True)
    vaccination_list = []
    for i in all_centrality_dic:
        vaccination_list.append(i[0])
        if len(vaccination_list) == amt_vaccination:
            break
    del all_centrality_dic
    gc.collect()
    return vaccination_list


def getDegreePoint(graph, amt_vaccination):
    """
    寻找网络度数中心性最大的部分点
    :param graph: 无向图
    :param amt_vaccination: 需要免疫的节点的数量
    :return: 返回amt_vaccination大小的list，里面代表对应需要免疫的节点
    """
    all_degree_dic = graph.degree()
    vaccination_list = []
    all_degree_dic = sorted(all_degree_dic.iteritems(), key=lambda asd: asd[1], reverse=True)
    for i in all_degree_dic:
        vaccination_list.append(i[0])
        if len(vaccination_list) == amt_vaccination:
            break
    del all_degree_dic
    gc.collect()
    return vaccination_list


def randWalk(graph, amt_vaccination, total):
    """
    使用random的方法，在整个网络中随机选择一个节点，寻找一条路径
    :param graph: 无向图
    :param amt_vaccination: 需要寻找的节点数目
    :param total: 原来网络中总的节点数（实验的网络是寻找的整个网络中最大连通子图，这样才能得到所有节点的标签）
    :return: 接种点集合
    """
    vaccination_list = []
    while True:
        current_position = random.randint(0, total)
        if current_position not in vaccination_list and current_position in graph.nodes():
            vaccination_list.append(current_position)
            if len(vaccination_list) == amt_vaccination:
                break
            next_path_list = (graph.neighbors(current_position))
            next_path_list = list(set(next_path_list).difference(set(vaccination_list)))
            if len(next_path_list) <= 0:
                continue
            index = random.uniform(0, 1)
            current_position = next_path_list[int(index * (len(next_path_list) - 1))]
            vaccination_list.append(current_position)
            if len(vaccination_list) == amt_vaccination:
                break
    return vaccination_list


def getRandSpanTree(graph, amt_vaccination, total, start_sign=0, diffusion_sign=0):
    """
    使用随机生成树的方法，在整个网络中随机选择一个节点，生成一颗生成树，再在生成树中寻找节点degree最大的部分杰斯按
    :param graph:
    :param amt_vaccination:
    :param total:
    :param start_sign: 生成树起始点的选择，0表示随机选择一个节点作为起始点，1表示的是选择一个度最大的节点作为起始点。  默认式0
    :param diffusion_sign: 使用方法的标志位置,如果是0表示使用的是随机的方式，1表示使用的节点度大的点作为扩散点   默认是0
    :return: 接种点集合
    """
    if start_sign == 0:
        while True:
            current_position = random.randint(0, total)
            if current_position in graph.nodes():
                break
    elif start_sign == 1:
        current_position = sorted((nx.degree(graph)).iteritems(), key=lambda b: b[1], reverse=True)[0][0]
    else:
        exit(0)
    vaccination_list = []
    travel_list = []  # 表示已经遍历过的点
    path_list = []  # 标识遍历的路线，当travelList长度等于总的点数的时候表示遍历完成
    path_list.append(current_position)
    travel_list.append(current_position)
    weight_list = [0 * i for i in range(total)]
    travel_list.append(current_position)
    while len(travel_list) < graph.number_of_nodes():  # 将所有点加入树中就是遍历结束的标志
        current_position = path_list[-1]
        next_path_list = graph.neighbors(current_position)
        next_path_list = list(set(next_path_list).difference(set(travel_list)))
        if len(next_path_list) == 0:  # 表示当前点没有邻居，遍历过程进行回退
            del path_list[-1]
        else:
            if diffusion_sign == 0:
                # 所有邻居中随机选择一个作为扩散点
                index = random.uniform(0, 1)
                next_position = next_path_list[int(index * (len(next_path_list) - 1))]
            elif diffusion_sign == 1:
                # 选择度最大的节点作为扩散点
                temp = 0
                next_position = next_path_list[0]
                for index in next_path_list:
                    if len(graph.neighbors(index)) > temp:
                        temp = len(graph.neighbors(index))
                        next_position = index
            else:
                exit(0)
            weight_list[current_position] += 1
            travel_list.append(next_position)
            path_list.append(next_position)
    order_weight_list = sorted(weight_list, reverse=True)
    for i in range(amt_vaccination):
        for j in range(total):
            if weight_list[j] == order_weight_list[i]:
                vaccination_list.append(j)
                weight_list[j] = 0
                break
    del order_weight_list, weight_list, travel_list, path_list
    gc.collect()
    return vaccination_list


def getRandNeiPoint(graph, amt_vaccination, total):
    """
    寻找随机点中所有邻居中度最大的点
    :param graph:
    :param amt_vaccination:
    :param total:
    :return: 接种点的集合
    """
    vaccination_list = []
    index_list = []
    while len(vaccination_list) < amt_vaccination:
        index = random.randint(0, total)
        if index not in index_list and index in graph.nodes():
            index_list.append(index)
            max_degree = 0  # 最大的度
            subscript = 0  # 度最大的节点的下标
            for i in graph.neighbors(index):
                count_nei = len(graph.neighbors(i))
                if count_nei >= max_degree:
                    max_degree = count_nei
                    subscript = i
            vaccination_list.append(subscript)
    return vaccination_list


def getRankByCluDe(graph, amt_vaccination, double_num):
    """
    一个检验函数，使用degree/clustering+double_num
    :param graph:
    :param amt_vaccination:
    :param double_num: 就是一个参数
    :return:
    """
    clu_dic = nx.clustering(graph)
    clu_dic = sorted([double(len(graph.neighbors(i))) / (clu_dic[i] + double_num) for i in clu_dic].iteritems(),
                     key=lambda d: d[1], reverse=True)
    del clu_dic
    gc.collect()
    vaccination_list = [clu_dic[j][0] for j in range(amt_vaccination)]
    return vaccination_list


def getRandNeiOfNeiPoint(graph, amt_vaccination, total):
    """
    寻找随机点中邻居的邻居中度最大的点
    :param graph:
    :param amt_vaccination:
    :param total:
    :return:
    """
    vaccination_list = []
    index_list = []
    while (len(vaccination_list) < amt_vaccination):
        nei_list = []  # 邻居的邻居
        index = random.randint(0, total)
        if index not in index_list:
            index_list.append(index)
            for i in graph.neighbors(index):  # 遍历随机点的邻居
                nei_list = nei_list + graph.neighbors(i)
            nei_list = list(set(nei_list))  # 去除重复的元素
            max_degree = 1  # 最大的邻居数量
            subscript = 0  # 保留度最大的点
            for j in nei_list:
                count_nei = len(graph.neighbors(j))
                if count_nei >= max_degree:
                    max_degree = count_nei
                    subscript = j
            if subscript not in vaccination_list:
                vaccination_list.append(subscript)
    return vaccination_list


def getRandRadiusPoint(graph, amt_vaccination, radius, total):
    """
    计算在随机点半径为radius的范围内度最大的点
    :param graph:
    :param amt_vaccination:
    :param radius:
    :param total:
    :return:
    """
    vaccination_list = []
    index_list = []
    while len(vaccination_list) < amt_vaccination:
        index = random.randint(0, total)
        all_point = []  # 存放在半径范围内的所有的点
        if index not in index_list:
            index_list.append(index)
            all_point.append(index)
            for i in range(radius):
                for j in all_point:
                    all_point = all_point + graph.neighbors(j)
            all_point = list(set(all_point))
            subscript = 0
            max_degree = 1  # 最大的邻居数量
            for i in all_point:
                count_nei = graph.neighbors(i)
                if count_nei >= max_degree:
                    max_degree = count_nei
                    subscript = i
            if subscript not in vaccination_list:
                vaccination_list.append(subscript)
    return vaccination_list


def getInfluence(graph, vaccination_list):
    """
    获取对应接种接种点之后的影响范围
    :param graph: 原图
    :param vaccination_list: 接种节点的集合
    :return: 删除对应节点之后的一个鲁帮性结果
    """
    influence_list = []
    for i in vaccination_list:
        graph.remove_edges_from(graph.edges(i))
        g = nx.connected_components(graph)  # 得到断开该点之后的连接情况
        count_graph = graph.number_of_nodes()
        influence_point = 0.0
        for j in g:
            count_sub_graph = len(j)  # 得到局部网络的人数
            influence_point = influence_point + double(count_sub_graph * count_sub_graph) / double(count_graph)
        influence_list.append(double(influence_point) / count_graph)
    return influence_list


def getRelativeSize(graph, vaccination_list):
    """
    获得最大簇的相对大小
    :param graph:
    :param vaccination_list: 待接种的点的集合
    :return: relative_size (= (最大簇的节点数量)/(网络总的节点数目))
    """
    count_nodes = graph.number_of_nodes()
    relative_size_list = []
    for i in vaccination_list:
        temp = 0
        graph.remove_edges_from(graph.edges(i))
        nx.connected_component_subgraphs(graph)
        for j in nx.connected_component_subgraphs(graph):
            if j.number_of_nodes() > temp:
                temp = j.number_of_nodes()
                new_graph = j
        relative_size_list.append(double(new_graph.number_of_nodes()) / count_nodes)
    return relative_size_list


def getInfo(graph, vaccination_list):
    """
    :param graph:
    :param vaccination_list:
    :return: list，[整个网络平均度，接种集合点的平均度，所有节点的品据聚类系数，接种集合点的平均聚类系数，所有点的平均k_shell,接种点的平均k-shell]
    """
    info_list = []
    count_nodes = graph.number_of_nodes()
    count_degree = 0
    for i in nx.degree(graph).values():
        count_degree += i
    info_list.append(double(count_degree) / double(count_nodes))
    count_degree = 0
    count_clustering = 0.0
    for i in vaccination_list:
        count_degree += nx.degree(graph, i)
        count_clustering += nx.clustering(graph, i)
    info_list.append(double(count_degree) / double(len(vaccination_list)))
    info_list.append(nx.average_clustering(graph))
    info_list.append(double(count_clustering) / double(len(vaccination_list)))
    total = 0
    index = 0
    shell = 1
    while True:
        if 0 == nx.k_shell(graph, shell).number_of_nodes():
            break
        total += nx.k_shell(graph, shell).number_of_nodes() * shell
        for j in vaccination_list:
            if j in nx.k_shell(graph, shell):
                index += shell
        shell += 1
    info_list.append(double(total) / double(count_nodes))
    info_list.append(double(index) / double(len(vaccination_list)))
    return info_list


def getRankByCluDe(graph, amt_vaccination):
    clu_dic = nx.clustering(graph)
    aver_clu = nx.average_clustering(graph)
    for i in clu_dic:
        clu_dic[i] = double(len(graph.neighbors(i))) / (clu_dic[i] + aver_clu)
    clu_dic = sorted(clu_dic.iteritems(), key=lambda d: d[1], reverse=True)
    vaccination_list = [clu_dic[j][0] for j in range(amt_vaccination)]
    return vaccination_list


def getRandWalkByRadius(graph, amt_vaccination, step_num):
    node_dic = {}
    for node in nx.nodes(graph):
        current_node = node
        temp_set = set([])
        for i in range(step_num):
            nei_node_list = graph.neighbors(current_node)
            current_node = nei_node_list[random.randint(0, len(nei_node_list))]
            temp_set.add(current_node)
        node_dic[node] = len(temp_set)
    return [sorted(node_dic.iteritems(), key=lambda records: records[1], reverse=True).keys()][0:amt_vaccination]
