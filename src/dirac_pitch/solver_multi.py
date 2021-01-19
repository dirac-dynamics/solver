# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 21:49:57 2020

@author: focke
"""
from __future__ import print_function
from ortools.graph import pywrapgraph
import numpy as np
import osmnx as ox
ox.config(use_cache=True, log_console=False)
# ox.__version__
import networkx as nx

#from utils import *

def set_trans_node(node_index):
    func_start_nodes = [node_index, node_index, node_index+3]
    func_end_nodes = [node_index+1, node_index+2, node_index+2]
    func_costs = [0, 0, 0]
    
    func_supplies = [0, -1, 0, 1]
    
    return func_start_nodes, func_end_nodes, func_costs, func_supplies


def simp_min_cost_flow(n_carrier,n_transportables,weights,connections,n_connections, transportables, targets, inter_dic, target_dic):
    

    min_cost_flow = pywrapgraph.SimpleMinCostFlow()

    """
    Define the directed graph for the flow.
    """
    #sink and carrier nodes
    supplies = np.concatenate(([(min(n_carrier,n_transportables))], np.zeros(n_carrier)))
    
    
    #arcs from sink to carriers
    start_nodes = np.zeros(n_carrier)
    
    end_nodes = np.linspace(1,n_carrier,n_carrier)
    
    costs = np.zeros(n_carrier)
    
    
    #arcs from carriers to transportables
    for i in range(n_carrier):
        start_nodes = np.concatenate((start_nodes , np.full(n_connections[i],i+1)))
        
    end_nodes = np.concatenate((end_nodes , connections))
    
    costs = np.concatenate((costs, weights))
    
    
    #arcs transportable intern
    for i in range(n_transportables):
        s_nodes, e_nodes, intern_costs, intern_supplies = set_trans_node(n_carrier+1+i*4)
        start_nodes = np.concatenate((start_nodes, s_nodes))
        end_nodes = np.concatenate((end_nodes, e_nodes))
        supplies = np.concatenate((supplies, intern_supplies))
        costs = np.concatenate((costs, intern_costs))
        
    
    #arcs between transportables + end
    for i in range(n_transportables):
        start_nodes = np.concatenate((start_nodes , np.full(n_transportables,n_carrier+1+2+i*4)))
        
    for i in range(n_transportables):
        end_node_list = []
        for j in range(n_transportables):
            if j==i:
                end_node_list.append(n_carrier+4*n_transportables+1)
            else:
                end_node_list.append(n_carrier+1+j*4)
            
        end_nodes = np.concatenate((end_nodes , end_node_list))
    

    
    for i in range(n_transportables):
        cost_list = []
        for j in range(n_transportables):
            if j==i:
                cost_list.append(target_dic['weight_list'][i])#(0)
            else:
                cost_list.append(inter_dic['weight_list_2'][i][j]+target_dic['weight_list'][i])
            
        costs = np.concatenate((costs , cost_list))
    
    #add end node supply
    supplies = np.concatenate((supplies,[-(min(n_carrier,n_transportables))]))

    # all paths have capacity 1
    capacities =np.zeros(len(start_nodes))+1


    #convert to integers
    start_nodes = start_nodes.astype(int)
    end_nodes = end_nodes.astype(int)
    capacities = capacities.astype(int)
    costs = costs.astype(int)
    supplies = supplies.astype(int)

    #convert to lists
    start_nodes = start_nodes.tolist()
    end_nodes = end_nodes.tolist()
    capacities = capacities.tolist()
    costs = costs.tolist()
    supplies = supplies.tolist()
    
    #set parameters
    source = 0
    sink = n_carrier+n_transportables*4+1
    tasks = n_transportables

    
    
    
    
    
    # Add each arc.
    for i in range(len(start_nodes)):
        min_cost_flow.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i],capacities[i], costs[i])
    # Add node supplies.

    for i in range(len(supplies)):
        min_cost_flow.SetNodeSupply(i, supplies[i])

    # Find the minimum cost flow between node 0 and node 10.
    output = []
    
    

    if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
        #   if min_cost_flow.SolveMaxFlowWithMinCost() == min_cost_flow.OPTIMAL:
        
        for arc in range(min_cost_flow.NumArcs()):

          # Can ignore arcs leading out of source or into sink.
          if min_cost_flow.Tail(arc)!=source and min_cost_flow.Head(arc)!=sink:

            # Arcs in the solution have a flow value of 1. Their start and end nodes
            # give an assignment of worker to task.

            if min_cost_flow.Flow(arc) > 0 and min_cost_flow.UnitCost(arc) > 0:
                print('vertex %d assigned to vertex %d.  Cost = %d' % (
                    min_cost_flow.Tail(arc),
                    min_cost_flow.Head(arc),
                    min_cost_flow.UnitCost(arc)))
                output.append([min_cost_flow.Tail(arc),min_cost_flow.Head(arc)])
        
        print()
        print('Total cost = ', min_cost_flow.OptimalCost())
    else:
        print('There was an issue with the min cost flow input.')

    return output, min_cost_flow.OptimalCost()
