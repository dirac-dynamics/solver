from __future__ import print_function
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np

ox.config(use_cache=True, log_console=True)


def plot_assigned_routes(Graph,car,trans,tar,opt,route_l,con_l,target_routes):
    nc = []
    ns = []
    for node in Graph.nodes():
        if node in car:
            nc.append('r')
            ns.append(80)
        elif node in trans:
            nc.append('g')
            ns.append(80)
        elif node in tar:
            nc.append('y')
            ns.append(80)
        else:
            nc.append('w')
            ns.append(0)
        
    routes_to_plot = []
    for element in opt:
        #print(element)
        #print(con_l)
        
        routes_to_plot.append(route_l[con_l.index(element)])
        
    routes_to_plot = np.concatenate((routes_to_plot, target_routes))

    fig,ax = ox.plot.plot_graph_routes(Graph,routes_to_plot,route_colors='w', show=True, close=False, node_color=nc, node_size=ns)
    
    fig.savefig('graph.png')
    