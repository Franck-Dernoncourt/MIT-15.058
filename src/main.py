'''    
Created on May 2, 2014

@summary: 15.058 project

Installation instructions (Windows 7 SP1 x64, Python 2.7 x64):
 - Download & Install numpy and setuptools: http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools
 - Configure your PATH variable to include e.g. C:\Python27\Scripts\
 - Open a new Command Prompt
 - Run easy_install networkx-1.8.1-py2.7.egg
 
'''

import networkx as nx
import numpy as np
#from scipy import stats

# Global parameters
infinite = 999999
shuttle_penalty = 300 # in seconds
walking_time_filename = '../data/CampusMatrix - Walking Time.csv' # time in seconds
shuttle_time_filename = '../data/CampusMatrix - Shuttle.csv' # time in seconds
outdoorness_filename = '../data/CampusMatrix - Outdoorness.csv' # binary: 0 is indoor, 1 is outdoor
shuttle_connection_time_filename = '../data/CampusMatrix - Shuttle-Connection.csv' # time in seconds. This separate matrix allows us to add a penalty when the user take the shuttle
    
def read_node_labels(filename):
    '''
    Read node labels from files
    '''
    fd = open(filename,'r')
    node_labels = fd.readline().split(',')[1:]
    node_labels[-1] = node_labels[-1].replace('\n', '') 
    fd.close()
    return node_labels

def convert_list_to_dict(my_list):
    '''
    Convert a list into a dictionary
    E.g. ['a', 'b'] -> {0: 'a', 1: 'b'}
    '''
    list2=range(len(my_list))
    my_dict = dict(zip(list2, my_list))
    return my_dict

def delete_first_row_and_column(array):
    '''
    Delete the first row and the first column of a numpy array
    http://stackoverflow.com/questions/3877491/deleting-rows-in-numpy-array
    '''
    new_array = np.delete(array, (0), axis=0) #  delete the first row
    new_array = np.delete(new_array, (0), axis=1) #  delete the first column
    return new_array

def replace_nan_to_infinite(array2D):
    '''
    Replace NaN by infinite in a 2D array
    '''
    for (x,y), value in np.ndenumerate(array2D): 
        if np.isnan(array2D[x][y]): array2D[x][y] = infinite        
    return array2D
        
        
def read_weights_from_file(filename):
    '''
    Read distances (e.g. edge weights) from file
    '''
    data = np.genfromtxt(filename, delimiter=',')
    data = replace_nan_to_infinite(delete_first_row_and_column(data))    
    return data

def compute_shortest_path(graph, target_node, source_node):
    '''
    
    '''
    print(nx.dijkstra_path(graph,source=source_node,target=target_node))
    print(nx.dijkstra_path_length(graph,source=source_node,target=target_node))

def add_penalty(array2D, penalty):
    '''
    Replace NaN by infinite in a 2D array
    '''
    for (x,y), value in np.ndenumerate(array2D): 
        if (array2D[x][y] <> 0) and (array2D[x][y] <> infinite):
            array2D[x][y] += penalty   
    return array2D

def main():
    '''
    This is the main function
    http://networkx.lanl.gov/reference/algorithms.operators.html
    '''    
    walking_times = read_weights_from_file(walking_time_filename)  
    shuttle_times = read_weights_from_file(shuttle_time_filename)
    shuttle_connection_times = read_weights_from_file(shuttle_connection_time_filename)
    shuttle_connection_times = add_penalty(shuttle_connection_times, shuttle_penalty/2) # /2 because we get in and out the shuttle, so we don't want to have a double penalty
    
    #print walking_times
    walking_graph = nx.DiGraph(data=walking_times)
    #print G.edges(data=True)
    walking_graph = nx.relabel_nodes(walking_graph,convert_list_to_dict(read_node_labels(walking_time_filename)))    
    print 'walking_graph', walking_graph.edges(data=True)
    
    shuttle_graph = nx.DiGraph(data=shuttle_times)
    shuttle_graph = nx.relabel_nodes(shuttle_graph,convert_list_to_dict(read_node_labels(shuttle_time_filename)))
    print 'shuttle_graph', shuttle_graph.edges(data=True)
    
    shuttle_connection_graph = nx.DiGraph(data=shuttle_connection_times)
    shuttle_connection_graph = nx.relabel_nodes(shuttle_connection_graph,convert_list_to_dict(read_node_labels(shuttle_connection_time_filename)))
    # add shuttle penalty
    print 'shuttle_connection_graph', shuttle_connection_graph.edges(data=True)
    
    # Create main graph
    main_graph = nx.compose(walking_graph, shuttle_graph)
    print 'main_graph', main_graph.edges(data=True)    
    main_graph = nx.compose(main_graph, shuttle_connection_graph)
    print 'main_graph', main_graph.edges(data=True)
    
    # Compute the shortest paths and path lengths between nodes in the graph.
    # http://networkx.lanl.gov/reference/algorithms.shortest_paths.html
    compute_shortest_path(main_graph, '32', 'NW86')
    
    # TODO: display travel time
    # TODO: outdoorness
    # TODO: enjoyability
    

def display_path_labels(node_labels, path):
    '''
    [42, 43, 44, 45, 48, 49, 52, 54] -> ['NW12', 'NW13', 'NW14', 'NW15', 'NW20', 'NW21', 'NW35', 'NW86']
    '''
    readable_path = []
    for node in path:
        readable_path.append(node_labels[node])
    return readable_path


if __name__ == "__main__":
    main()
    
    
    '''
    Garbage:
    
    A=np.matrix([[1,99],[1,1]])    
    G = nx.DiGraph(data=A)
    print G.edges(data=True)
    
    print(nx.dijkstra_path(G,source=0,target=30))
    print(nx.dijkstra_path_length(G,source=0,target=30))
    print(nx.dijkstra_path(G,source=node_labels.index('NW86'),target=node_labels.index('32')))
    print(nx.dijkstra_path_length(G,source=node_labels.index('NW86'),target=node_labels.index('32')))
    
    print(nx.dijkstra_path(G,source=node_labels.index('1'),target=node_labels.index('76')))
    print(nx.dijkstra_path_length(G,source=node_labels.index('1'),target=node_labels.index('76')))
    
    print(display_path_labels(node_labels, nx.dijkstra_path(G,source=node_labels.index('1'),target=node_labels.index('76'))))
    print(display_path_labels(node_labels, nx.dijkstra_path(G,source=node_labels.index('NW12'),target=node_labels.index('NW86'))))
    print(nx.dijkstra_path(G,source=node_labels.index('NW12'),target=node_labels.index('NW86')))
    print(nx.dijkstra_path_length(G,source=node_labels.index('NW12'),target=node_labels.index('NW86')))

    '''