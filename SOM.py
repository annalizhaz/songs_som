from SOMMapper import SOMMapper
from Node import Node

from UMatrixMapper import UMatrixMapper
import sys
import csv

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
        with open("u_matrix.txt", "w") as file_name:
            for line in runner.stream_output():
                (x, y), value = job.parse_output_line(line)
                print(value)
                file_name.write(str(value))

    def get_u_matrix(self):
        self.write_nodes_to_file()

        compute_u_matrix_job = UMatrixMapper(args = ["node_list.csv", "--map", "map_file.csv"])

        with compute_u_matrix_job.make_runner() as compute_u_matrix_runner:
            compute_u_matrix_runner.run()
            self.extract_u_matrix(compute_u_matrix_job, compute_u_matrix_runner)




if __name__ == "__main__":
    file_name = sys.argv[2]
    n = int(sys.argv[1])
    ## file in remaining parameters

    som_map = SOM(n)
    grid = som_map.train_map(file_name)

    som_map.get_u_matrix()

    #UMatrix(grid)