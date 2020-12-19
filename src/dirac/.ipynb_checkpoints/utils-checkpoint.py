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
        

