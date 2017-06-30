import argparse
import csv
import matplotlib
matplotlib.use("Agg") ## for remote run
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
import numpy as np
from SOMMapper import SOMMapper
from UMatrixMapper import UMatrixMapper
from Node import Node


class SOM:

    def __init__(self, n, x_len, y_len, epochs, theta_f):
        '''
        x_len, y_len: grid size
        n: vectors length (i.e. number of attributes in dataset)
        epochs: number of iterations
        theta_naught, theta_f: decay learning constants
        grid: Node grid
        '''
        self.x_len = x_len
        self.y_len = y_len
        self.n = n
        self.epochs = epochs
        self.theta_naught = math.sqrt(self.x_len * self.y_len)
        self.learning_factor = theta_f / self.theta_naught

        self.grid = [[Node(i, j, self.n) for i in range(self.x_len)] for j in range(self.y_len)]

        ## File names used incidentally during execution
        self.map_file_name = "map_file.csv"
        self.nodes_file_name = "node_list.csv"
        self.u_matrix_output = "u_matrix.png"


    def train_map(self, input_file):
        for i in range(self.epochs):
            ## Set neighborhood width to exponential decay
            theta = self.theta_naught * (self.learning_factor ** (i / self.epochs))

            ## Write current grid to file
            with open(self.map_file_name, "w") as file_name:
                writer = csv.writer(file_name)
                writer.writerows(self.grid)

            ## For every training vector, calculate grid node weights
            compute_weights_job = SOMMapper(args = [str(input_file), "--map", 
                str(self.map_file_name), "--n", str(self.n), "--theta", str(theta)])

            ## Read output from SOMMapper
            with compute_weights_job.make_runner() as compute_weights_runner:
                compute_weights_runner.run()
                self.extract_weights(compute_weights_job, compute_weights_runner)


    def extract_weights(self, job, runner):
        ## Helper function to extract SOMMapper output
        for line in runner.stream_output():
            (x, y), value = job.parse_output_line(line)
            ## Update grid weigts
            self.grid[x][y].update_weights(value)

    
    def get_u_matrix(self):
        ## Write current grid to file
        self.write_nodes_to_file()

        ## Calculate the u-matrix height of each grid node
        compute_u_matrix_job = UMatrixMapper(args = [str(self.nodes_file_name), 
            "--map", str(self.map_file_name)])

        ## Read output from UMatrixMapper
        with compute_u_matrix_job.make_runner() as compute_u_matrix_runner:
            compute_u_matrix_runner.run()
            matrix = self.extract_u_matrix(compute_u_matrix_job, compute_u_matrix_runner)
        
        return matrix


    def write_nodes_to_file(self):
        ## Helper function to write each grid node's Cartesian coordinates 
        ## and weights to file
        with open(self.nodes_file_name, "w") as file_name:
            writer = csv.writer(file_name)

            for i, row in enumerate(self.grid):
                for j, node in enumerate(row):
                    writer.writerow([i, j] + node.weights)


    def extract_u_matrix(self, job, runner):
        ## Helper function to extract UMatrixMaper output
        u_matrix = [[0] * self.y_len for x in range(self.x_len)]
        for line in runner.stream_output():
            (x, y), value = job.parse_output_line(line)
            u_matrix[x][y] = value
        return np.array(u_matrix)


    def get_bmus(self, vector_list):
        ## Calculate BMUs for a list of vectors
        bmus = [Node.compute_winning_vector(self.grid, x) for x in vector_list]
        return np.array(bmus)


    '''
    Graph function adapted from Peter Wittek: https://github.com/peterwittek/somoclu
    '''
    def graph_umatrix(self, matrix, bmus = None, labels = None):
        plt.clf()
        plt.imshow(matrix, aspect = "auto", cmap = cm.coolwarm)
        plt.axis("off")

        ## Set colorbar legend
        cmap = cm.ScalarMappable(cmap = cm.coolwarm)
        cmap.set_array(matrix)
        plt.colorbar(cmap, orientation = "vertical", shrink = .7)

        ## Add scatter points to graph representing vector BMUs
        if bmus is not None:
            plt.scatter(bmus[:, 0], bmus[:, 1], c = "gray")

        ## Add labels to vector scatter points
        if labels is not None:
            for label, col, row in zip(labels, bmus[:, 0], bmus[:, 1]):
                plt.annotate(label, xy = (col, row), xytext = (10, -5), 
                    textcoords = "offset points", ha = "left", va = "bottom", 
                    bbox = {"boxstyle": "round", "fc": "lightgray"})
    
        plt.savefig(self.u_matrix_output)


if __name__ == "__main__":
    ## Define and collect command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help = "file name of song vectors")
    parser.add_argument("n", type = int, help = "length of vector attributes")
    parser.add_argument("--x_len", default = 10, type = int, help = "number of grid rows")
    parser.add_argument("--y_len", default = 10, type = int, help = "number of grid columns")
    parser.add_argument("--epochs", default = 15, type = int, help = "number of iterations")
    parser.add_argument("--theta_f", default = .2, type = float, help = "exponential decay constant")
    args = parser.parse_args()

    ## Create and train map
    som_map = SOM(args.n, args.x_len, args.y_len, args.epochs, args.theta_f)
    som_map.train_map(args.file_name)

    ## Create and save u-matrix
    matrix = som_map.get_u_matrix()
    som_map.graph_umatrix(matrix)

    #goatwhore = [0, 0.2946608101, 0.0603604847]
    #throbbing_gristle = [0, 0.4670240136, 0.0830032339]
    #britney_spears = [0.9930382894, 0.3205599089, 0.0480877322]
    #labels = ["Goatwhore", "Throbbing Gistle", "Britney Spears"]
    #bmus = som_map.get_bmus([goatwhore, throbbing_gristle, britney_spears])