'''    
Created on May 2, 2014

@summary: 15.058 project

Installation instructions:
Download & Install numpy and setuptools: http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools
Configure your PATH variable to include e.g. C:\Python25\Scripts\
Open a new Command Prompt
Run easy_install networkx-1.8.1-py2.7.egg
'''

import networkx as nx
import numpy as np
#from scipy import stats

def main():
    '''
    This is the main function
    '''
    # Parameters
    infinite = 999999
    walking_time_filename = '../data/CampusMatrix - Walking Time.csv' # time in seconds
    
    # Get node labels
    fd = open(walking_time_filename,'r')
    node_labels = fd.readline().split(',')[1:]
    fd.close()
    
    # Read distance data
    walking_time_data = np.genfromtxt(walking_time_filename, delimiter=',')
    #print walking_time_data    
    walking_times = np.delete(walking_time_data, (0), axis=0) #  delete the first row: http://stackoverflow.com/questions/3877491/deleting-rows-in-numpy-array
    walking_times = np.delete(walking_times, (0), axis=1) #  delete the first column
    #print walking_times
    
    # Replace NaN by infinite
    for (x,y), value in np.ndenumerate(walking_times): 
        if np.isnan(walking_times[x][y]): walking_times[x][y] = infinite
    
    #print walking_times
    G = nx.DiGraph(data=walking_times)
    print G.edges(data=True)
    
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