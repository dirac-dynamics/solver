from __future__ import print_function
# import .utils
from utils import *
from solver import *
from plot import *

from ortools.graph import pywrapgraph
import time
import os
import random as rng
import multiprocessing as mp
import numpy as np
import osmnx as ox
import matplotlib.pyplot as plt
import copy
import networkx as nx

ox.config(use_cache=True, log_console=True)
# ox.__version__

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
    
    print()
    print('Classical network flow solver:')
    print()

    optimal_routes, cost_solver = simp_min_cost_flow(len(carriers),
                                        len(transportables),
                                        dic['weight_list'],
                                        dic['connection_list'],
                                        dic['connection_number'])

   

    plot_assigned_routes(G, carriers, transportables, optimal_routes, dic['route_list'], dic['end_list'], dic['carrier_number'])
    

    print()
    print('Greedy 1 solver:')
    print()
    
    weight_list_2_copy = copy.deepcopy(dic['weight_list_2'])
    end_list_copy = copy.deepcopy(dic['end_list'])

    optimal_routes, cost_greedy_1=greedy_algo(weight_list_2_copy,end_list_copy,carrier_number, transportable_number)

    plot_assigned_routes(G, carriers, transportables, optimal_routes, dic['route_list'], dic['end_list'], dic['carrier_number'])

    
    print()
    print('Greedy 2 solver:')
    print()

    weight_list_2_copy = copy.deepcopy(dic['weight_list_2'])
    start_end_list_copy = copy.deepcopy(dic['start_end_list'])
    
    optimal_routes, cost_greedy_2=greedy_algo_2(weight_list_2_copy,start_end_list_copy,carrier_number, transportable_number)

    plot_assigned_routes(G, carriers, transportables, optimal_routes, dic['route_list'], dic['end_list'], dic['carrier_number'])
    
    
    print()
    print()
    print('Improvement to greedy 1: %2f' % ((1-cost_solver/cost_greedy_1)*100) + ' %')
    print('Improvement to greedy 2: %2f' % ((1-cost_solver/cost_greedy_2)*100) + ' %')




create_from_city('munich', 10, 10)
