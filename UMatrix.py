from scipy.spatial import distance
from Node import Node

def UMatrix(node_list, filename = "u_matrix.txt"):
    '''
    weight_map is a list of lists of lists
    '''
    for node in node_list:
        x = node.x
        y = node.y
        neighbors = []
        total_dst = 0
        u_vals = []
        for n_node in node_list:
            if n_node.x in range(x-1, x+2) and n_node.y in range(y-1, y+2):
                neighbors.append(n_node)
        
        for n_node in neighbors:
            total_dst += node.calculate_distance(n_node)
            '''
            a = tuple(node.weights)
            b = tuple(n_node.weights)
            total_dst += distance.euclidean(a,b)
            '''
            
        node.u_val = total_dst/len(neighbors)

        u_vals.append(node.u_val)
        u_string = " ".join(u_vals)

    text_file = open(filename, "w")
    text_file.write(u_string)
    text_file.close()
 
 #def bmu():