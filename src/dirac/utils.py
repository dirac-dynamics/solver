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
from collections import OrderedDict, defaultdict


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
        
def fetch_city_2(name,north,south,east,west):
    if isinstance(name, str):
        data = json.load(open('../maps/places.json'))
        if name in data:
            graph = ox.io.load_graphml(data[name])
            print('Graph loaded..')
            
        else:
            print('Fetching graph..')
            graph = ox.graph.graph_from_bbox(north, south, east, west, network_type='drive')
            ox.io.save_graphml(graph, filepath='../maps/%s.graphml' % (name))
            data[name] = '../maps/%s.graphml' % (name)
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
        
        ox.speed.add_edge_speeds(graph, hwy_speeds=speeds, fallback=50, precision=1)
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


def set_objects(G, carrier_number, transportable_number, random=True, carrier_list=None, transportable_list=None):
    
    #number of entities
    carrier_number = carrier_number
    transportable_number = transportable_number
    G = G
    
    if random == True:
    #functions to select random nodes
        def create_random_node_points(number,Graph):
            node_list=[]
            for i in range(number):
                node_list.append(rng.randint(0,len(list(G.nodes))-1))
            return node_list
        
        carriers = create_random_node_points(carrier_number,G)
        transportables = create_random_node_points(transportable_number,G)
        print('Random entities generated..')
    else:
        carriers = []
        transportables = []
        for i, carrier in enumerate(carrier_list):
            carriers.append(ox.distance.get_nearest_node(G, (carrier[0],carrier[1])))
                            
        for i, transportable in enumerate(transportable_list):
            transportables.append(ox.distance.get_nearest_node(G, (transportable[0],transportable[1])))
        print('Entities loaded from input..')
    #create random carriers and transportables
    
    
    return G, carriers, transportables
    
    
def find_paths(G, carriers, transportables):
    
    dic = defaultdict(lambda: [])
    
    dic['node_info'] = G.nodes

    for i, carrier in enumerate(carriers):
        temp_dic = defaultdict(lambda: [])
        counter = 0
        for j, transportable in enumerate(transportables):

            #if (ox.distance.euclidean_dist_vec(dic['node_info'][carrier]['y'],
            #                                   dic['node_info'][carrier]['x'],
            #                                   dic['node_info'][transportable]['y'],
            #                                   dic['node_info'][transportable]['x'])) <= 0.15:

                dic['connection_list'].append(j+1+len(carriers))
                temp_dic['end_numbers'].append(j)
                temp_dic['start_to_end'].append([i,j])
                way = ox.shortest_path(G, carrier, transportable, weight='travel_time')
                temp_dic['ways_to_transportable'].append(way)
                way_weight = 0

                for k in range(len(way)-1):
                    way_weight += G[way[k]][way[k+1]][0]['travel_time']
                    
                dic['weight_list'].append(int(way_weight))
                temp_dic['weights_to_transportables'].append(int(way_weight))
                counter+=1

        dic['end_list'].append(temp_dic['end_numbers'])
        dic['connection_number'].append(counter)
        dic['route_list'].append(temp_dic['ways_to_transportable'])
        dic['weight_list_2'].append(temp_dic['weights_to_transportables'])
        dic['start_end_list'].append(temp_dic['start_to_end'])
        
    print('Paths found..')
        
    return G, dic


def output_routes(Graph,opt_routes,dic):
        index_routes = []
        coord_routes = []
        for element in opt_routes:
            index_routes.append(dic['route_list'][element[0]-1][dic['end_list'][element[0]-1].index(element[1]-1)])
            
        for route in index_routes:
            coord_route = []
            for i, node_index in enumerate(route):
                coord_route.append((dic['node_info'][node_index]['y'],dic['node_info'][node_index]['x']))
            coord_routes.append(coord_route)
        return coord_routes