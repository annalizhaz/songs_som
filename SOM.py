from SOMMapper import SOMMapper
from Node import Node

from UMatrixMapper import UMatrixMapper
import sys
import csv

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class SOM:
    def __init__(self, n, x_len = 10, y_len = 10, epochs = 10, theta_naught = 10, theta_f = .2):
        '''
        x_len, y_len: size of grid
        n: size of vectors (number of attributes in data)
        epochs: number of iterations
        theta_naught, theta_f: learning constants
        map: Node grid
        '''
        self.x_len = x_len
        self.y_len = y_len
        self.n = n
        self.map = [[Node(i, j, self.n) for i in range(self.x_len)] for j in range(self.y_len)]
        self.epochs = epochs
        self.theta_naught = theta_naught
        self.learning_factor = theta_f / theta_naught

    def extract_weights(self, job, runner):
        for line in runner.stream_output():
            (x, y), value = job.parse_output_line(line)
            self.map[x][y].update_weights(value)
            print("({},{}) = {}".format(x, y, value))

    def train_map(self, file_name):
        ## Initalize time variable t
        for i in range(self.epochs):
            ## Set width exponential decay
            theta = self.theta_naught * (self.learning_factor ** (i / self.epochs))

            ## Write current weight map to file
            with open("map_file.csv", "w") as map_file:
                writer = csv.writer(map_file)
                writer.writerows(self.map)

            compute_weights_job = SOMMapper(args = [str(file_name), "--map", "map_file.csv", "--theta", str(theta), "--n", str(self.n)])

            with compute_weights_job.make_runner() as compute_weights_runner:
                compute_weights_runner.run()
                self.extract_weights(compute_weights_job, compute_weights_runner)

        return self.map


    def write_nodes_to_file(self):
        with open("node_list.csv", "w") as map_file:
                writer = csv.writer(map_file)

                for i, row in enumerate(self.map):
                    for j, node in enumerate(row):
                        writer.writerow([i,j]+node.weights)

    def extract_u_matrix(self, job, runner):
        u_matrix = [[0] * self.y_len for x in range(self.x_len)]
        for line in runner.stream_output():
            (x, y), value = job.parse_output_line(line)
            u_matrix[x][y] = value
        return np.array(u_matrix)

        with open("u_matrix.txt", "w") as file_name:
                writer = csv.writer(file_name, delimiter = " ")
                writer.writerows(u_matrix)

    def get_u_matrix(self):
        self.write_nodes_to_file()

        compute_u_matrix_job = UMatrixMapper(args = ["node_list.csv", "--map", "map_file.csv"])

        with compute_u_matrix_job.make_runner() as compute_u_matrix_runner:
            compute_u_matrix_runner.run()
            matrix = self.extract_u_matrix(compute_u_matrix_job, compute_u_matrix_runner)
            return matrix

    def u_matrix_from_file(self, file_name): 
        matrix = []
        with open(file_name) as f:
            reader = csv.reader(f, delimiter = " ")
            for row in reader:
                matrix.append([float(x) for x in row])
        return np.array(matrix)

    '''
    def get_single_bmu(self, node):
        return SOMMapper.compute_winning_vector(node)
    '''

    '''
    Graph functions drawn from peterwittek/somoclu
    '''

    def view_umatrix(self, matrix, bmus = None, labels = None):

        #zoom = ((0, self.x_len), (0, self.y_len))
        #figsize = (8, 8/float(zoom[1][1]/zoom[0][1]))
        #fig = plt.figure() #figsize = figsize)
        plt.clf()

        plt.imshow(matrix) #[0:self.y_len, 0:self.x_len], aspect = "auto")
        plt.set_cmap(cm.coolwarm)

        cmap = cm.ScalarMappable(cmap=cm.coolwarm)
        cmap.set_array(matrix)
        plt.colorbar(cmap, orientation = "vertical", shrink = .7)

        if bmus != None:
            plt.scatter(bmus[:, 0], bmus[:, 1], c="gray")


            for label, col, row in zip(labels, bmus[:, 0], bmus[:, 1]):
                if label != None:
                    plt.annotate(label, xy=(col, row), xytext=(10, -5),
                                 textcoords='offset points', ha='left',
                                 va='bottom',
                                 bbox=dict(boxstyle='round,pad=0.3',
                                           fc='white', alpha=0.8))
    

        plt.axis("off")
        plt.savefig("u_matrix5.png")

    def get_bmu(self, vector_input):
        min_distance = 1
        bmu = (0, 0)
        for i, row in enumerate(self.map):
            for j, node in enumerate(row):
                distance = node.calculate_distance(vector_input)
                ## Update best matching unit
                if min_distance > distance:
                    min_distance = distance
                    bmu = (i, j)
        return bmu

    def get_bmus(self, vector_list):
        bmus = []
        for vector in vector_list:
            bmus.append(self.get_bmu(vector))
        return np.array(bmus)


if __name__ == "__main__":
    file_name = sys.argv[2]
    n = int(sys.argv[1])
    ## file in remaining parameters

    #som_map = SOM(n)
    #grid = som_map.train_map(file_name)

    #matrix = som_map.get_u_matrix()
    #som_map.view_umatrix(matrix)

    #song_a = [0.9791148682, 0.4183931491,0.0484596353]
    #song_b = [0, 0.2690661652, 0.0919894148]
    #song_c = [0.9915464943, 0.4234423412, 0.0692342276]
    #labels = ["song a", "song b", "song c"]
