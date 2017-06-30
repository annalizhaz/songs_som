from mrjob.job import MRJob
from mrjob.step import MRStep
from Node import Node


class UMatrixMapper(MRJob):

    def configure_options(self):
        super(UMatrixMapper, self).configure_options()
        self.add_file_option("--map")


    def load_weights(self):
        ## Load grid weights from file
        self.grid = Node.get_map(self.options.map)


    def calculate_neighborhood(self, _, cell_string):
        ## Load grid weights
        grid = Node.get_map(self.options.map)
        
        ## Extract weight vectors from passed cell
        cell = cell_string.split(",")
        x_coord = int(cell[0])
        y_coord = int(cell[1])
        weights = [float(x) for x in cell[2:]]
        ## Construct node object
        node = Node(x_coord, y_coord, len(weights), weights)

        ## Calculate neighbors' distance
        for i in range(max(0, x_coord - 1), min(len(self.grid), x_coord + 2)):
            for j in range(max(0, y_coord - 1), min(len(self.grid[0]), y_coord + 2)):
                distance = self.grid[i][j].calculate_distance(weights)
                yield((x_coord, y_coord), distance)


    def calculate_height(self, grid_key, distances):
        distances = list(distances)
        yield(grid_key, sum(distances) / len(distances))


    def steps(self):
        return [MRStep(mapper_init = self.load_weights,
                       mapper = self.calculate_neighborhood,
                       reducer = self.calculate_height)]


if __name__ == "__main__":
    UMatrixMapper.run()