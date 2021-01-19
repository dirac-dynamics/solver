# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:44:13 2021

@author: focke
"""
from __future__ import print_function
from ortools.graph import pywrapgraph
#import time
import os
import random as rng
#import multiprocessing as mp
import numpy as np
import osmnx as ox
import matplotlib.pyplot as plt
import copy
ox.config(use_cache=True, log_console=False)
ox.__version__
import networkx as nx
import json
from collections import OrderedDict, defaultdict


        
def fetch_city(name,north,south,east,west):
    if isinstance(name, str):
        print('Fetching graph..')
        data = json.load(open('../maps/places.json'))
        if name in data:
            graph = ox.io.load_graphml(data[name])
            print('Graph loaded..')
            
        else:
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
    print('Deleting dead ends..')

    #graph = ox.project_graph(graph)
    graph = ox.consolidate_intersections(graph, tolerance=0.0000001, dead_ends=False)

    #graph = ox.consolidate_intersections(graph, rebuild_graph=True, tolerance=1, dead_ends=False)
    
    print('Dead ends deleted..')
    
    return graph
        

def set_speed(graph, german=False):
    
    # not: sets pre-set speed limits
    # fills up unknown speed-limits according to their type
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


def set_objects(G, carrier_list, transportable_list, target_list):

    carriers = []
    transportables = []
    targets = []
    for i, carrier in enumerate(carrier_list):
        carriers.append(ox.distance.get_nearest_node(G, (carrier[0],carrier[1])))
                            
    for i, transportable in enumerate(transportable_list):
        transportables.append(ox.distance.get_nearest_node(G, (transportable[0],transportable[1])))
            
    for i, target in enumerate(target_list):
        targets.append(ox.distance.get_nearest_node(G, (target[0],target[1])))
    print('Entities loaded from input..')

    return carriers, transportables, targets


def find_first_paths(G, carriers, transportables):
    
    print('Finding initial paths to transportables..')
    
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

                dic['connection_list'].append(j*4+1+len(carriers))
                dic['connection_list_single'].append(j+1+len(carriers))
                temp_dic['end_numbers'].append(j)
                temp_dic['start_to_end'].append([i,j])
                dic['plot_start_end'].append([i+1,len(carriers)+1+j*4])
                way = ox.shortest_path(G, carrier, transportable, weight='travel_time')
                temp_dic['ways_to_transportable'].append(way)
                dic['plot_route'].append(way)
                way_weight = 0
                way_length = 0

                for k in range(len(way)-1):
                    way_weight += G[way[k]][way[k+1]][0]['travel_time']
                    way_length += G[way[k]][way[k+1]][0]['length']
                    
                dic['weight_list'].append(int(way_weight))
                temp_dic['length_of_routes'].append(int(way_length))
                temp_dic['weights_to_transportables'].append(int(way_weight))
                counter+=1

        dic['end_list'].append(temp_dic['end_numbers'])
        dic['connection_number'].append(counter)
        dic['route_list'].append(temp_dic['ways_to_transportable'])
        dic['weight_list_2'].append(temp_dic['weights_to_transportables'])
        dic['start_end_list'].append(temp_dic['start_to_end'])
        dic['length_list'].append(temp_dic['length_of_routes'])
        
    print('Initial paths found..')
        
    return dic


def find_inter_paths(G, transportables, targets, n_carrier):
    
    print('Finding paths between delivery points and transportables..')
    
    dic = defaultdict(lambda: [])
    
    dic['node_info'] = G.nodes

    for i, start_trans in enumerate(targets):
        temp_dic = defaultdict(lambda: [])
        counter = 0
        for j, end_trans in enumerate(transportables):

            #if (ox.distance.euclidean_dist_vec(dic['node_info'][carrier]['y'],
            #                                   dic['node_info'][carrier]['x'],
            #                                   dic['node_info'][transportable]['y'],
            #                                   dic['node_info'][transportable]['x'])) <= 0.15:

                dic['connection_list'].append(j*4+1+n_carrier)
                temp_dic['end_numbers'].append(j)
                temp_dic['start_to_end'].append([i,j])
                dic['plot_start_end'].append([n_carrier+1+i*4+2,n_carrier+1+j*4])
                way = ox.shortest_path(G, start_trans, end_trans, weight='travel_time')
                temp_dic['ways_to_transportable'].append(way)
                dic['plot_route'].append(way)
                way_weight = 0
                way_length = 0

                for k in range(len(way)-1):
                    way_weight += G[way[k]][way[k+1]][0]['travel_time']
                    way_length += G[way[k]][way[k+1]][0]['length']
                    
                dic['weight_list'].append(int(way_weight))
                temp_dic['length_of_routes'].append(int(way_length))
                temp_dic['weights_to_transportables'].append(int(way_weight))
                counter+=1

        dic['end_list'].append(temp_dic['end_numbers'])
        dic['connection_number'].append(counter)
        dic['route_list'].append(temp_dic['ways_to_transportable'])
        dic['weight_list_2'].append(temp_dic['weights_to_transportables'])
        dic['start_end_list'].append(temp_dic['start_to_end'])
        dic['length_list'].append(temp_dic['length_of_routes'])

        
    print('Interconnecting paths found..')
    
    return dic
    
    
def find_trans_paths(G, transportables, targets):
    
    print('Finding paths from pickup to delivery..')
    
    dic = defaultdict(lambda: [])
    
    dic['node_info'] = G.nodes

    for i in range(len(transportables)):
        temp_dic = defaultdict(lambda: [])
        
        way = ox.shortest_path(G, transportables[i], targets[i], weight='travel_time')
        dic['route_list'].append(way)
        way_weight = 0
        way_length = 0

        for k in range(len(way)-1):
            way_weight += G[way[k]][way[k+1]][0]['travel_time']
            way_length += G[way[k]][way[k+1]][0]['length']
                    
        dic['weight_list'].append(int(way_weight))
        dic['length_list'].append(int(way_length))
                
        
    print('Paths for transportables found..')
        
    return dic



def get_route_start_end_node(opt_route_list,carriers,targets,transportables):
        route_start_end_node = []
        for element in opt_route_list:
            start_end_array=[]
            if element[0]<=len(carriers):

                start_end_array.append(carriers[element[0]-1])
            else:

                start_end_array.append(targets[int((element[0]-1-len(carriers)-2)/4)])
                

            start_end_array.append(transportables[int((element[1]-1-len(carriers))/4)])

            
            route_start_end_node.append(start_end_array)
        
        return(route_start_end_node)
    

    
def get_coord_routes(G,route_nodes,first_routes, target_routes, inter_routes, carriers):
        node_routes = []
        for car in carriers:
            car_routes=[]
            for element in route_nodes:
                if element[0]==car:
                    
                    
                    for sublist in first_routes:
                        for subsublist in sublist:
                            if subsublist[0] == car and subsublist[-1] == element[1]:
                                car_routes.append(subsublist)
                                break
                                break
                    route_nodes.remove(element)
                    break
            for sublist in target_routes:
                if sublist[0] == car_routes[-1][-1]:
                    car_routes.append(sublist)
                    break
            i=0
            while i < len(route_nodes):
                if route_nodes[i][0]==car_routes[-1][-1]:
                    
                    for sublist in inter_routes:
                        for subsublist in sublist:
                            if subsublist[0] == car_routes[-1][-1] and subsublist[-1] == route_nodes[i][1]:
                                car_routes.append(subsublist)
                                break
                                break
                        
                    for sublist in target_routes:
                        if sublist[0] == car_routes[-1][-1]:
                            car_routes.append(sublist)
                            break
                    
                    route_nodes.remove(route_nodes[i])
                    i=0
                else:
                    i+=1
            node_routes.append(car_routes)
        
        real_coords = []    
        for path in node_routes:
            path_array = []
            for route in path:
                route_array = []
                for node in route:
                    route_array.append((G.nodes[node]['y'],G.nodes[node]['x']))
                path_array.append(route_array)
            real_coords.append(path_array)
            
        return real_coords,node_routes
  
    
def get_time_length(graph,coord_route):
        time = 0
        length = 0
        for k in range(len(coord_route)-1):
            time += graph[coord_route[k]][coord_route[k+1]][0]['travel_time']
            length += graph[coord_route[k]][coord_route[k+1]][0]['length']
        return time,length
    

    
def get_routes_time_length(graph,coord_route_list):
        all_time=[]
        all_length=[]
        for path in coord_route_list:
            path_time=[]
            path_length=[]
            for route in path:
                time,length=get_time_length(graph,route)
                path_time.append(time)
                path_length.append(length)
            all_time.append(path_time)
            all_length.append(path_length)
        return all_time,all_length
    
    
def output_routes(Graph,opt_routes,dic):
        index_routes = []
        coord_routes = []
        all_time=[]
        all_length=[]
        for element in opt_routes:
            index_routes.append(dic['route_list'][element[0]-1][dic['end_list'][element[0]-1].index(element[1]-1)])
            
        for route in index_routes:
            coord_route = []
            for i, node_index in enumerate(route):
                coord_route.append((dic['node_info'][node_index]['y'],dic['node_info'][node_index]['x']))
            coord_routes.append(coord_route)
            time = 0
            length = 0
            for k in range(len(route)-1):
                time += Graph[route[k]][route[k+1]][0]['travel_time']
                length += Graph[route[k]][route[k+1]][0]['length']
            all_time.append(time)
            all_length.append(length)
            
        return coord_routes, all_time, all_length
    

def output_lengths(opt_routes,dic):
        overall_length = 0
        for element in opt_routes:
            overall_length += dic['length_list'][element[0]-1][dic['end_list'][element[0]-1].index(element[1]-1)]
            
        return overall_length