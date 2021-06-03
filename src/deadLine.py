from os import replace
from pprint import pprint
import networkx as nx
import pandas as pd

def create_blocks():
    solve = {}
    solve["Г1"] = ['г'+str(i) for i in range(100, 110)] + ['г'+str(i)+j for i in [106, 109, 110, 111] for j in ['-1', '-2']]
    solve["Г2п"] = ["г" + str(i) for i in range(211, 232)] + ['г'+i+j for i in ['226', '227'] for j in ['-1','-2']]
    solve['Г2л'] = ['г' + str(i) for i in range(201, 211)]+['г232']
    solve['г3п'] = ['г' + str(i) for i in range(309, 327)]
    solve['г3л'] = ['г' + str(i) for i in range(301, 309)] + ['г327']
    solve['г4п'] = ['г' + str(i) for i in range(415, 428)]
    solve['г4л'] = ['г' + str(i) for i in range(401, 415)] + ['г' + str(i) for i in range(429, 431)]

    solve['в2п'] = ['в' + str(i) for i in range(213,223)] 
    solve['в2л'] = ['в' + str(i) for i in range(201,212)] + ['в223']
    solve['в3п'] = ['в' + str(i) for i in range(316,332)] 
    solve['в3л'] = ['в' + str(i) for i in range(301,314)]
    solve['в4п'] = ['в' + str(i) for i in range(410,422)] + ['в435'] 
    solve['в4л'] = ['в' + str(i) for i in range(401,410)] + ['в422', 'в423']

    solve['б1п'] = ['б' + str(i) for i in range(111,116)] 
    solve['б1л'] = ['б' + str(i) for i in range(101,111)] + ['б116']
    solve['б2п'] = ['б' + str(i) for i in range(209,221)] 
    solve['б2л'] = ['б' + str(i) for i in range(201,209)] + ['б221']
    solve['б3п'] = ['б' + str(i) for i in range(316,328)] 
    solve['б3л'] = ['б' + str(i) for i in range(301,311)]
    solve['б4п'] = ['б' + str(i) for i in range(401,413)]
    solve['б4л'] = ['б' + str(i) for i in range(414,426)]


    solve['д2п'] = ['д' + str(i) for i in range(211,226)] 
    solve['д2л'] = ['д' + str(i) for i in range(201,211)]
    solve['д3п'] = ['д' + str(i) for i in range(311,324)] 
    solve['д3л'] = ['д' + str(i) for i in range(301,311)]

    solve['и2п'] = ['и' + str(i) for i in range(201,207)] 
    solve['и2л'] = ['и' + str(i) for i in range(207,216)]

    solve['и1'] = ['и' + str(i) for i in range(100, 107)]

    solve['а1л'] = ['а'+str(i) for i in range(173,199)]
    solve['а1ц'] = ['а'+str(i) for i in range(129, 138, 2)] +  ['а'+str(i) for i in range(156, 172)]
    solve['а1п'] = ['а'+str(i) for i in range(100,125)] + ['а'+str(i) for i in range(126, 139, 2)]

    solve['а2лл'] = ['а'+ str(i) for i in range(217, 236)] + ['а7', "а8"]
    solve['а2лц'] = ['а' + str(i) for i in [5, 6, 214, 215, 216]]
    solve['а2пц'] = ['а' + str(i) for i in [3, 4, 211, 212, 213]]
    solve['а2пп'] = ['а'+ str(i) for i in range(202, 210)] + ['а1', "а2"]

    solve['а3лл'] = ['а'+ str(i) for i in range(323, 337)] + ['а17', "а18"]
    solve['а3лц'] = ['а' + str(i) for i in [14, 15, 16, 319, 320, 321, 322]]
    solve['а3пц'] = ['а' + str(i) for i in [11, 12, 13, 315, 316, 317, 318]]
    solve['а3пп'] = ['а'+ str(i) for i in range(300, 315)] + ['а9', "а10"]

    solve['а4л'] = ['а'+str(i) for i in range(425,439)]
    solve['а4ц'] = ['а'+str(i) for i in range(416, 425)] 
    solve['а4п'] = ['а'+str(i) for i in range(402,413)]
    return solve

def my_func(start, end):
    G = nx.DiGraph()
    message = ""
    blocks = create_blocks()
    
    keys = {'Г1': "Корпус Г, первый этаж", "лг": "Лестница корпуса Г", "пкг" : "Переход в корпус Г", "шт" : "Штаны", "пкд":"Переход в корпус Д", "лд":"Лестница корпуса Д", "д2л":"Корпус Д второй этаж, при выходе с лестницы налево"}
    start_key = end_key = None

    for key in blocks:
        if start in blocks[key]:
            start_key = key
        if end in blocks[key]:
            end_key = key

    if (start_key == None or end_key == None):
        if start_key == None:
            message += "Аудитория "+start+" не найдена.\n"
        if end_key == None:
            message += "Аудитория "+end+" не найдена.\n"
        return message


    edges = []

    df = pd.read_excel('table.xlsx', engine='openpyxl')
    for i in range(56):
        for j in range(56):
            if df.iloc[(i, j)] != -1:
                edges.append((df.columns[i], df.columns[j], 1))

    G.add_weighted_edges_from(edges)

    # расчет кратчайших путей для ВСЕХ пар вершин
    predecessors, _ = nx.floyd_warshall_predecessor_and_distance(G)
    # кратчайший путь от вершины [s] к вершине [v]
    shortest_path = nx.reconstruct_path(start_key, end_key, predecessors)
    shortest_path = [keys[i] for i in shortest_path]
    message = "Маршрут между [{}] и [{}]:\n{}"\
            .format(start, end, "\n".join(shortest_path))
    return message
