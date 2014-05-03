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
walking_time_filename = '../data/CampusMatrix - Walking Time.csv' # time in seconds
shuttle_time_filename = '../data/CampusMatrix - Shuttle.csv' # time in seconds
outdoorness_filename = '../data/CampusMatrix - Outdoorness.csv' # binary: 0 is indoor, 1 is outdoor
    
def read_node_labels():
    '''
    Read node labels from files
    '''
    fd = open(walking_time_filename,'r')
    node_labels = fd.readline().split(',')[1:]
    fd.close()
    return node_labels

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
        
        
def read_shuttle_data():
    '''
    Read distances (e.g. edge weights) from file
    '''
    shuttle_time_data = np.genfromtxt(shuttle_time_filename, delimiter=',')
    shuttle_times = replace_nan_to_infinite(delete_first_row_and_column(shuttle_time_data))    
    return shuttle_times

def read_distance_data():
    '''
    Read distances (e.g. edge weights) from file
    '''
    # Read distance data
    walking_time_data = np.genfromtxt(walking_time_filename, delimiter=',')
    walking_times = replace_nan_to_infinite(delete_first_row_and_column(walking_time_data))    
    
    
    return walking_times

def main():
    '''
    This is the main function
    http://networkx.lanl.gov/reference/algorithms.operators.html
    '''    
    node_labels = read_node_labels()
    walking_times = read_distance_data()  
    shuttle_times = read_shuttle_data() 
    
    #print walking_times
    G = nx.DiGraph(data=walking_times)
    print G.edges(data=True)
    shuttle_graph = nx.DiGraph(data=shuttle_times)
    print shuttle_graph.edges(data=True)
    
    # TODO: add edge name somehow
    #print nx.union(G, shuttle_graph)
    
    # Compute the shortest paths and path lengths between nodes in the graph.
    # http://networkx.lanl.gov/reference/algorithms.shortest_paths.html
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
    '''