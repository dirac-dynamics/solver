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
ox.config(use_cache=True, log_console=True)
ox.__version__
import networkx as nx
import util


# def create_from_city(city, carriers, transportables, average=True, dead_ends=True, ):
    
#     G = 
    
#     # create graph
#     G = ox.io.load_graphml('/maps/munich.graphml')
#     G = nx.convert_node_labels_to_integers(G)