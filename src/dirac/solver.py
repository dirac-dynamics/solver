# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 16:00:33 2020

@author: Niels Focke
"""
from __future__ import print_function
from ortools.graph import pywrapgraph
import numpy as np
import osmnx as ox
ox.config(use_cache=True, log_console=False)
# ox.__version__
import networkx as nx


# def network_solver(carriers, transportables, weight_list):
#     ALI_G = nx.DiGraph()
#     counter = 0
#
#     for j, trans in enumerate(transportables):
#         ALI_G.add_node(trans, demand = 1)
#
#     for i, car in enumerate(carriers):
#         ALI_G.add_node(car, demand = -1)
#
#     for i, car in enumerate(carriers):
#         for j, trans in enumerate(transportables):
#             ALI_G.add_edge(car, trans, weight=int(weight_list[counter]), capacity=1)
#             counter += 1
#
#     flowDict_alt = nx.min_cost_flow(G)
#     #TODO: How to read the data?


def simp_min_cost_flow(n_carrier,n_transportables,weights,connections,n_connections):
    

    min_cost_flow = pywrapgraph.SimpleMinCostFlow()


    # Define the directed graph for the flow.
    start_nodes = np.zeros(n_carrier)
    for i in range(n_carrier):
        start_nodes = np.concatenate((start_nodes , np.full(n_connections[i],i+1)))
    start_nodes = np.concatenate((start_nodes , np.linspace(n_carrier+1,n_carrier+n_transportables,n_transportables)))

    end_nodes = np.linspace(1,n_carrier,n_carrier)
    end_nodes = np.concatenate((end_nodes , connections))
    end_nodes = np.concatenate((end_nodes , np.full(n_transportables,n_carrier+n_transportables+1)))

    capacities =np.zeros(n_carrier+sum(n_connections)+n_transportables)+1

    costs = np.concatenate((np.zeros(n_carrier), weights, np.zeros(n_transportables)))

    start_nodes = start_nodes.astype(int)
    end_nodes = end_nodes.astype(int)
    capacities = capacities.astype(int)
    costs = costs.astype(int)

    start_nodes = start_nodes.tolist()
    end_nodes = end_nodes.tolist()
    capacities = capacities.tolist()
    costs = costs.tolist()

    source = 0
    sink = n_carrier+n_transportables+1
    tasks = n_transportables

    supplies = np.concatenate(([min(n_carrier,n_transportables)], np.zeros(n_carrier+n_transportables),[-min(n_carrier,n_transportables)]))
    supplies = supplies.astype(int)
    supplies = supplies.tolist()

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

            if min_cost_flow.Flow(arc) > 0:
                print('Carrier %d assigned to transportable %d.  Cost = %d' % (
                    min_cost_flow.Tail(arc),
                    min_cost_flow.Head(arc)-n_carrier,
                    min_cost_flow.UnitCost(arc)))
                output.append([min_cost_flow.Tail(arc),min_cost_flow.Head(arc)-n_carrier])
        
        print()
        print('Total cost = ', min_cost_flow.OptimalCost())
    else:
        print('There was an issue with the min cost flow input.')

    return output, min_cost_flow.OptimalCost()


def greedy_algo(weights, ends, car_num, trans_num):
    overall_cost = 0
    output = []
    for i in range(min([car_num,trans_num])):
        picked_index = weights[i].index(min(weights[i]))
        picked_end =  ends[i][picked_index]
        overall_cost += weights[i][picked_index]
        output.append([i+1,picked_end+1])
        print('Carrier %d assigned to transportable %d.  Cost = %d' % (
                i+1,
                picked_end+1,
                weights[i][picked_index]))
        for j in range(len(ends)):
            if picked_end in ends[j]:
                index=ends[j].index(picked_end)
                del ends[j][index]
                del weights[j][index]
    print()
    print('Total cost = ',overall_cost)
    return output, overall_cost



def greedy_algo_2(weights, connects, car_num, trans_num):
    overall_cost = 0
    output = []
    for i in range(min([car_num,trans_num])):
        zipped = zip(weights, connects)
        new_zipped = sorted(zipped, key = lambda t: min(t[0]))
        weights,connects = zip(*new_zipped)
        weights =list(weights)
        connects =list(connects)
        picked_index = weights[0].index(min(weights[0]))
        picked_connect =  connects[0][picked_index]
        overall_cost += weights[0][picked_index]
        output.append([picked_connect[0]+1,picked_connect[1]+1])
        print('Carrier %d assigned to transportable %d.  Cost = %d' % (
                picked_connect[0]+1,
                picked_connect[1]+1,
                weights[0][picked_index]))
        for j in range(len(connects)):
            for k in range(len(connects[j])):
                if picked_connect[1] == connects[j][k][1]:
                    del connects[j][k]
                    del weights[j][k]
                    break
        del connects[0]
        del weights[0]
    print()
    print('Total cost = ',overall_cost)
    return output, overall_cost
    