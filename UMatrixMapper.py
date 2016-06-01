from mrjob.job import MRJob
from mrjob.step import MRStep
from Node import Node

import math
import csv

class UMatrixMapper(MRJob):

    def configure_options(self):
        super(UMatrixMapper, self).configure_options()
        self.add_file_option("--map")

    def calculate_neighborhood(self, _, row):
        grid = Node.get_map(self.options.map)
        row = row.split(",")

        x_coord = int(row[0])
        y_coord = int(row[1])
        weights = [float(x) for x in row[2:]]

        node = Node(x_coord, y_coord, len(weights), weights)

        for i in range(max(0, x_coord - 1), min(len(grid), x_coord + 2)):
            for j in range(max(0, y_coord - 1), min(len(grid[0]), y_coord + 2)):
                distance = grid[i][j].calculate_distance(weights)
                #print("({},{}) - {}".format(x_coord, y_coord, distance))
                yield((x_coord, y_coord), distance)


    def accumlate_denominator(self, grid_key, distances):
        distances = list(distances)
        u = sum(distances) / len(distances)

        yield(grid_key, u)



    def steps(self):
        return [MRStep(mapper = self.calculate_neighborhood,
                       #combiner = self. ,
                       reducer = self.accumlate_denominator)]

if __name__ == "__main__":
    UMatrixMapper.run()