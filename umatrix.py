from scipy.spatial import distance

def umatrix(node_list, filename):
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
			a = tuple(node.weights)
			b = tuple(n_node.weights)
			total_dst += distance.euclidean(a,b)
			
		node.u_val = total_dst/len(neighbors) #add this to node class

		u_vals.append(node.u_val)
		u_string = " ".join(u_vals)

	text_file = open(filename, "w")
	text_file.write(u_string)
	text_file.close()
	return

def bmu():