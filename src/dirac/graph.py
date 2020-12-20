from __future__ import print_function
from utils import *
from solver import *
from plot import *

import time
import random as rng
import osmnx as ox
import networkx as nx

ox.config(use_cache=True, log_console=True)

# functions to select random nodes


def create_random_node_points(number, graph):
    node_list = []
    for i in range(number):
        node_list.append(rng.randint(0, len(list(graph.nodes)) - 1))
    return node_list


def create_from_city(city,
                     carrier_number,
                     transportable_number,
                     random=True,
                     average=True,
                     dead_ends=True,
                     carrier_list=None,
                     transportable_list=None):
    # loads graph
    G = fetch_city(city)

    if not dead_ends:
        G = no_dead_ends(G)

    G = set_speed(G, german=True)

    G = nx.convert_node_labels_to_integers(G)
    node_info = G.nodes

    carrier_number = carrier_number
    transportable_number = transportable_number

    # # TODO: Write else for input lists and catch for exception
    # if random:
    #     # create random carriers and transportables
    #     carriers = create_random_node_points(carrier_number, G)
    #     transportables = create_random_node_points(transportable_number, G)

    G, carriers, transportables = set_objects(G, carrier_number, transportable_number)

    # find paths from carriers to transportables
    G, dic = find_paths(G, carriers, transportables)

    optimal_routes = simp_min_cost_flow(len(carriers),
                                        len(transportables),
                                        dic['weight_list'],
                                        dic['connection_list'],
                                        dic['connection_number'])

    # print()
    # print("Time =", time.process_time() - start_time, "seconds")
    # print()
    # print(optimal_routes)
    start_time = time.process_time()

    # plotting routine
    color_list = ['r', 'b', 'g', 'y']
    # color_list=['C00','C01','C02','C03','C04','C05']
    plot_assigned_routes(G, carriers, transportables, optimal_routes, dic['route_list'], dic['end_list'], dic['carrier_number'])

    print()
    print("Time =", time.process_time() - start_time, "seconds")
    print()
    start_time = time.process_time()


create_from_city('munich', 10, 10)
