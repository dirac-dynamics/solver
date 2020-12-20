# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 16:00:33 2020

@author: Niels Focke
"""
from __future__ import print_function
from ortools.graph import pywrapgraph
import time
import os
import random as rng
import multiprocessing as mp
import numpy as np
import osmnx as ox
import matplotlib.pyplot as plt
ox.config(use_cache=True, log_console=False)
ox.__version__
import networkx as nx



def simp_min_cost_flow(number_carriers, numbers_carriers, weights, number_connections):
    

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

    costs = np.concatenate((np.zeros(n_carrier), weight_list, np.zeros(n_transportables)))

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
    print('Total cost = ', min_cost_flow.OptimalCost())
    print()
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
            output.append([min_cost_flow.Tail(arc),min_cost_flow.Head(arc)])
    else:
    print('There was an issue with the min cost flow input.')

    return output
    