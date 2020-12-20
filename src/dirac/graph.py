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
import util





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
    
    G = set_speed(graph, german=False)
    
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
    
    node_info = node_info
    route_list = []
    weight_list = []
    weight_list_2 = []

    connection_list = []
    connection_number = []
    end_list = []
    start_end_list =[]

    for i in range(len(carriers)):
        ways_to_transportables = []
        weights_to_transportables = []
        start_to_end = []
        end_numbers = []
        counter=0
        for j in range(len(transportables)):
                connection_list.append(j+1+carrier_number)
                end_numbers.append(j)
                start_to_end.append([i,j])
                way = ox.shortest_path(G2, carriers[i], transportables[j], weight='travel_time')
                ways_to_transportables.append(way)
                way_weight=0
                for k in range(len(way)-1):
                    way_weight += (G2[way[k]][way[k+1]][0]['travel_time'])
                weight_list.append(way_weight)
                weights_to_transportables.append(way_weight)
                counter+=1

        end_list.append(end_numbers)
        connection_number.append(counter)
        route_list.append(ways_to_transportables)
        weight_list_2.append(weights_to_transportables)
        start_end_list.append(start_to_end)
    
    