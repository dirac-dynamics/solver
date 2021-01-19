# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:36:36 2021

@author: focke
"""
from __future__ import print_function
#print('test')
# import .utils
from utils import *

import utils_osmnx as uo


from ortools.graph import pywrapgraph
import time
import os

import numpy as np

import osmnx as ox
import matplotlib.pyplot as plt
import copy
import networkx as nx

ox.config(use_cache=True, log_console=True)

#%%
def setup_osmnx(city, north, south, east, west,
                     carrier_list,
                     transportable_list,
                     target_list,
                     dead_ends=True):
    G = uo.fetch_city(city, north, south, east, west)

    if not dead_ends:
        G = uo.no_dead_ends(G)

    G = uo.set_speed(G, german=True)

    G = nx.convert_node_labels_to_integers(G)

    carrier_number = len(carrier_list)
    transportable_number = len(transportable_list)

    # # TODO: Write else for input lists and catch for exception
    # if random:
    #     # create random carriers and transportables
    #     carriers = create_random_node_points(carrier_number, G)
    #     transportables = create_random_node_points(transportable_number, G)

    carriers, transportables, targets = uo.set_objects(G, carrier_list, transportable_list, target_list)
    
    print(carriers)
    print(targets)
    print(transportables)
    

    #if not dead_ends:
    #    G = no_dead_ends(G)

    # find paths from carriers to transportables
    dic = uo.find_first_paths(G, carriers, transportables)
    inter_dic = uo.find_inter_paths(G, transportables, targets, len(carriers))
    target_dic = uo.find_trans_paths(G, transportables, targets)
    
    
    solver_dic = defaultdict(lambda: [])
    
    solver_dic['dic']=dic
    solver_dic['inter_dic']=inter_dic
    solver_dic['target_dic']=target_dic
    solver_dic['G']=G
    #solver_dic['carrier_number']=carrier_number
    #solver_dic['transportable_number']=transportable_number
    solver_dic['carriers']=carriers
    solver_dic['targets']=targets
    solver_dic['transportables']=transportables

    return solver_dic

"""    
def setup_singlesolver_osmnx():
    


def setup_multisolver_google():
    
    
    
def setup_singlesolver_google():
"""  
    