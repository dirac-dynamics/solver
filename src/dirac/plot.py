from __future__ import print_function
import osmnx as ox
ox.config(use_cache=True, log_console=True)


def plot_assigned_routes(Graph,car,trans,opt,route_l,end_l,car_num):
    nc = []
    ns = []
    for node in Graph.nodes():
        if node in car:
            nc.append('r')
            ns.append(80)
        elif node in trans:
            nc.append('g')
            ns.append(80)
        else:
            nc.append('w')
            ns.append(0)
        
    routes_to_plot = []
    for element in opt:
        routes_to_plot.append(route_l[element[0]-1][end_l[element[0]-1].index(element[1]-1)])

    ox.plot.plot_graph_routes(Graph,routes_to_plot,route_colors='w', show=True, close=False, node_color=nc, node_size=ns)