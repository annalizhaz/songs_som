import math
from mrjob.job import MRJob
from mrjob.step import MRStep
from Node import Node


class SOMMapper(MRJob):

    def configure_options(self):
        super(SOMMapper, self).configure_options()
        self.add_passthrough_option("--n", type = "int")
        self.add_passthrough_option("--theta", type = "float")
        self.add_file_option("--map")

<<<<<<< HEAD
    def load_weights(self):
        ## Load grid weights from file
        self.grid = Node.get_map(self.options.map)

    def calculate_neighborhood(self, _, input_vector):
=======

    def calculate_neighborhood(self, _, input_vector):
        ## Load grid weights
        grid = Node.get_map(self.options.map)

>>>>>>> fa02d979ac4a7f8cbd08bbad907167fa5b79a9f3
        ## Extract weight vectors from passed fields
        input_vector = [float(x) for x in input_vector.split(",")][1:]

        ## Find BMU
<<<<<<< HEAD
        x, y = Node.compute_winning_vector(self.grid, input_vector)

        ## Calculate Gausian neighborhood function for all grid nodes
        for i, row in enumerate(self.grid):
=======
        x, y = Node.compute_winning_vector(grid, input_vector)

        ## Calculate Gausian neighborhood function for all grid nodes
        for i, row in enumerate(grid):
>>>>>>> fa02d979ac4a7f8cbd08bbad907167fa5b79a9f3
            for j, node in enumerate(row):
                coor_distance = (i - int(x)) ** 2 + (j - int(y)) ** 2

                denominator = math.exp(-coor_distance / self.options.theta ** 2)
                numerator = [denominator * x for x in input_vector]

                yield((i, j), (numerator, denominator))


    def sum_ratios(self, grid_key, ratios):
        ratios = list(ratios)
        ## Initalize numerator, denominator of parallel weight function
        numerator = [0] * self.options.n
        denominator = 0
        
        ## Sum numerator, denominator
        for ratio in ratios:
            numerator = list(map(sum, zip(numerator, ratio[0])))
            denominator = denominator + ratio[1]

        yield(grid_key, [numerator, denominator])


    def calculate_ratios(self, grid_key, ratio):
        ratio = list(ratio)[0]
        yield(grid_key, [x / ratio[1] for x in ratio[0]])


    def steps(self):
<<<<<<< HEAD
        return [MRStep(mapper_init = self.load_weights,
                       mapper = self.calculate_neighborhood,
=======
        return [MRStep(mapper = self.calculate_neighborhood,
>>>>>>> fa02d979ac4a7f8cbd08bbad907167fa5b79a9f3
                       combiner = self.sum_ratios,
                       reducer = self.sum_ratios),
                MRStep(reducer = self.calculate_ratios)]


if __name__ == "__main__":
    SOMMapper.run()