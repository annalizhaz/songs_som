from mrjob.job import MRJob
from mrjob.step import MRStep
from Node import Node
import math
import csv

class SOMMapper(MRJob):

    def configure_options(self):
        super(SOMMapper, self).configure_options()
        self.add_passthrough_option("--theta", type = "float")
        self.add_passthrough_option("--n", type = "int")
        self.add_file_option("--map")



    def compute_winning_vector(self, input_vector):
        ## Find min distance over K nodes
        grid = Node.get_map(self.options.map)

        min_distance = grid[0][0].calculate_distance(input_vector)
        bmu = (0, 0)
        for i, row in enumerate(grid):
            for j, node in enumerate(row):
                distance = node.calculate_distance(input_vector)
                ## Update best matching unit
                if min_distance > distance:
                    min_distance = distance
                    bmu = (i, j)
        return bmu

    def accumulate_weights(self, _, input_vector):
        grid = Node.get_map(self.options.map)
        input_vector = [float(x) for x in input_vector.split(",")][1:]
        x, y = self.compute_winning_vector(input_vector)
        ## Accumulate numerator and denominator in weight equation over K nodes
        for i, row in enumerate(grid):
            for j, node in enumerate(row):
                coor_distance = (i - int(x)) ** 2 + (j - int(y)) ** 2

                denominator = math.exp(-coor_distance / self.options.theta ** 2)
                numerator = [denominator * x for x in input_vector]

                yield((i, j), (numerator, denominator))

    def accumlate_denominator(self, grid_key, ratios):
        temp = list(ratios)

        numerator = [0] * self.options.n
        denominator = 0

        for song in temp:
            numerator = list(map(sum, zip(numerator, song[0])))
            denominator = denominator + song[1]

        yield(grid_key, (numerator, denominator))

    def accumulate_numerator(self, grid_key, ratio):
        temp = list(ratio)[0]
        weight = [x / temp[1] for x in temp[0]]
        yield(grid_key, weight)

    def steps(self):
        return [MRStep(mapper = self.accumulate_weights,
                       combiner = self.accumlate_denominator,
                       reducer = self.accumlate_denominator),
                MRStep(reducer = self.accumulate_numerator)]

if __name__ == "__main__":
    SOMMapper.run()