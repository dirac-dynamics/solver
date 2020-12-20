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
ox.config(use_cache=True, log_console=False)
ox.__version__
import networkx as nx
import json


def fetch_city(city):
     if isinstance(city, str):
            
        data = json.load(open('../maps/places.json'))
        if city in data:
            graph = ox.io.load_graphml(data[city])
            print('Graph loaded..')
            
        else:
            print('Fetching graph..')
            graph = ox.graph_from_place(city,network_type='drive')
            ox.io.save_graphml(graph, filepath='../maps/%s.graphml' % (city))
            data[city] = '../maps/%s.graphml' % (city)
            with open('../maps/places.json', 'w') as outfile:
                json.dump(data, outfile)
                
            print('Graph loaded..')
        return graph

    else:
        raise TypeError("City must be string")

        
def no_dead_ends(graph):
    # deletes dead_end roads
    graph = ox.consolidate_intersections(graph, rebuild_graph=True, tolerance=1, dead_ends=False)
    
    print('Dead ends deleted..')
    
    return graph
        

def set_speed(graph, german=False):
    
    # sets pre-set speed limits
    if german: 
        speeds = {'motorway' : 80,
                   'trunk' : 80,
                   'primary' : 70,
                   'secondary' : 50,
                   'motorway_link' : 50,
                   'trunk_link' : 50,
                   'primary_link' : 50,
                   'secondary_link' : 50}
        
        ox.speed.add_edge_speeds(graph, hwy_speeds=speed_dict, fallback=50, precision=1)
        ox.speed.add_edge_travel_times(graph, precision=1)
    
    # takes pre-existing speed limits and fills up all unkown
    else:
        graph = ox.add_edge_speeds(graph)
        graph = ox.add_edge_travel_times(graph)
        speeds = {'residential': 35,
              'secondary': 50,
              'tertiary': 60}
        graph = ox.add_edge_speeds(graph, speeds)
        graph = ox.add_edge_travel_times(graph)
        
    print('Speed added..')
    return graph