from __future__ import print_function
from ortools.graph import pywrapgraph
import time
import os
import random as rng
import multiprocessing as mp
import numpy as np
import osmnx as ox
import matplotlib.pyplot as plt
import copy
ox.config(use_cache=True, log_console=True)
ox.__version__
import networkx as nx
import utils
import solver
import plot
import graph





#functions to select random nodes
def create_random_node_points(number,Graph):
    node_list=[]
    for i in range(number):
        node_list.append(rng.randint(0,len(list(node_info))-1))
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
    G = fetch_city(city, dead_ends=dead_ends)
    
    if not dead_ends:
        G = no_dead_ends(G)
    
    G = set_speed(graph, german=True)
    
    G = nx.convert_node_labels_to_integers(G)
    node_info = G.nodes
    
    carrier_number = carrier_number
    transportable_number = transportable_number
    
    #TODO: Write else for input lists and catch for exception
    if random:
        #create random carriers and transportables
        carriers = create_random_node_points(carrier_number,G)
        transportables = create_random_node_points(transportable_number,G)
    
    #find paths from carriers to transportables
    G, dic = find_paths(G, carriers, transportables)
    
    
    
    optimal_routes = simp_min_cost_flow(len(carriers),
                                        len(transportables),
                                        dic['weight_list'],
                                        dic['connection_list'],
                                        dic['connection_number'])
    
    print()
    print("Time =", time.process_time() - start_time, "seconds")
    print()
    #print(optimal_routes)
    start_time = time.process_time()

    #plotting routine
    color_list=['r','b','g','y']
    #color_list=['C00','C01','C02','C03','C04','C05']

    plot_assigned_routes(G2, carriers, transportables, optimal_routes, route_list, end_list, carrier_number)
    
    print()
    print("Time =", time.process_time() - start_time, "seconds")
    print()
    start_time = time.process_time()


    
    
create_from_city('munich', 10, 10)