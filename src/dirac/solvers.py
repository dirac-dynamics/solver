# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:17:09 2021

@author: focke
"""
from __future__ import print_function

import setup as stp
import utils_osmnx as uo
import solver_multi as sm
import solver_single as ss
import plot_single as sp
import plot_multi as mp

from ortools.graph import pywrapgraph
import time
import os
import random as rng
#import multiprocessing as mp
import numpy as np
#print('test')
import osmnx as ox
import matplotlib.pyplot as plt
import copy
import networkx as nx

ox.config(use_cache=True, log_console=True)

#%%
def multisolver_osmnx(solv_dic):
    
    dic = solv_dic['dic']
    inter_dic = solv_dic['inter_dic']
    target_dic = solv_dic['target_dic']
    G = solv_dic['G']

    carriers = solv_dic['carriers']
    targets = solv_dic['targets']
    transportables = solv_dic['transportables']
    
    carrier_number = len(carriers)
    transportable_number = len(transportables)
    
    print()
    print('Classical network flow solver:')
    print()

    optimal_routes_solv, cost_solver = sm.simp_min_cost_flow(carrier_number,
                                        transportable_number,
                                        dic['weight_list'],
                                        dic['connection_list'],
                                        dic['connection_number'],
                                        np.array(transportables),
                                        np.array(targets),
                                        inter_dic,
                                        target_dic)

    #print(optimal_routes_solv)    
    
    plot_route_list = np.concatenate((dic['plot_route'], inter_dic['plot_route']))
    plot_connection_list = np.concatenate((dic['plot_start_end'], inter_dic['plot_start_end'])).tolist()
    
    #mp.plot_assigned_routes(G, carriers, transportables, targets, optimal_routes_solv, plot_route_list, plot_connection_list, target_dic['route_list'])
    
    all_routes_coord, all_routes_node = uo.get_coord_routes(G,uo.get_route_start_end_node(optimal_routes_solv,carriers,targets,transportables),dic['route_list'],target_dic['route_list'],inter_dic['route_list'],carriers)

    all_routes_time, all_routes_length = uo.get_routes_time_length(G,all_routes_node)

    return all_routes_coord, all_routes_time, all_routes_length


#%%
def singlesolver_osmnx(solv_dic):
    dic = solv_dic['dic']
    G = solv_dic['G']

    carriers = solv_dic['carriers']
    targets = solv_dic['targets']
    transportables = solv_dic['transportables']
    
    carrier_number = len(carriers)
    transportable_number = len(transportables)
    
    print()
    print('Classical network flow solver:')
    print()

    optimal_routes_solv, cost_solver = ss.simp_min_cost_flow(carrier_number,
                                        transportable_number,
                                        dic['weight_list'],
                                        dic['connection_list_single'],
                                        dic['connection_number'])
    
    coord_routes_solv = uo.output_routes(G,optimal_routes_solv,dic)

    #sp.plot_assigned_routes(G, carriers, transportables, optimal_routes_solv, dic['route_list'], dic['end_list'], dic['carrier_number'])
    
    return coord_routes_solv


#%%
def greedy_singlesolver_osmnx(solv_dic):
    dic = solv_dic['dic']
    G = solv_dic['G']
    
    carriers = solv_dic['carriers']
    targets = solv_dic['targets']
    transportables = solv_dic['transportables']
    
    carrier_number = len(carriers)
    transportable_number = len(transportables)
    
    print()
    print('Greedy 2 solver:')
    print()

    weight_list_2_copy = copy.deepcopy(dic['weight_list_2'])
    start_end_list_copy = copy.deepcopy(dic['start_end_list'])
    
    optimal_routes_greed, cost_greedy= ss.greedy_algo(weight_list_2_copy,start_end_list_copy,carrier_number, transportable_number)
    
    coord_routes_greed =  uo.output_routes(G,optimal_routes_greed,dic)

    #sp.plot_assigned_routes(G, carriers, transportables, optimal_routes_greed, dic['route_list'], dic['end_list'], dic['carrier_number'])

    return coord_routes_greed

#%%

carrier_list = []
transportable_list = []
target_list = []

for i in range(rng.randint(2,2)):
    carrier_list.append((48.143743 + 0.05 * (rng.random() * 2 - 1),11.575942 + 0.10 * (rng.random() * 2 - 1)))
    
for i in range(rng.randint(4,4)):    
    transportable_list.append((48.143743 + 0.05 * (rng.random() * 2 - 1),11.575942 + 0.10 * (rng.random() * 2 - 1)))
    target_list.append((48.143743 + 0.05 * (rng.random() * 2 - 1),11.575942 + 0.10 * (rng.random() * 2 - 1)))

#%%
zwischen_dic = stp.setup_osmnx('munich_2', 48.143743 + 0.05, 48.143743 - 0.05, 11.575942 + 0.10, 11.575942 - 0.10, carrier_list, transportable_list, target_list, dead_ends=True)
#%%
print(multisolver_osmnx(zwischen_dic))
print(singlesolver_osmnx(zwischen_dic))
print(greedy_singlesolver_osmnx(zwischen_dic))