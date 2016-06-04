from mrjob.job import MRJob
from mrjob.step import MRStep
from Node import Node


class UMatrixMapper(MRJob):

    def configure_options(self):
        super(UMatrixMapper, self).configure_options()
        self.add_file_option("--map")


<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> da7317c3b80c6c17b1241f64414b1e0e16a7ed3d
    def load_weights(self):
        ## Load grid weights from file
        self.grid = Node.get_map(self.options.map)


    def calculate_neighborhood(self, _, cell_string):       
<<<<<<< HEAD
=======
    def calculate_neighborhood(self, _, cell_string):
        ## Load grid weights
        grid = Node.get_map(self.options.map)
        
>>>>>>> fa02d979ac4a7f8cbd08bbad907167fa5b79a9f3
=======
>>>>>>> da7317c3b80c6c17b1241f64414b1e0e16a7ed3d
        ## Extract weight vectors from passed cell
        cell = cell_string.split(",")
        x_coord = int(cell[0])
        y_coord = int(cell[1])
        weights = [float(x) for x in cell[2:]]
        ## Construct node object
        node = Node(x_coord, y_coord, len(weights), weights)

        ## Calculate neighbors' distance
<<<<<<< HEAD
<<<<<<< HEAD
        for i in range(max(0, x_coord - 1), min(len(self.grid), x_coord + 2)):
            for j in range(max(0, y_coord - 1), min(len(self.grid[0]), y_coord + 2)):
                distance = self.grid[i][j].calculate_distance(weights)
=======
        for i in range(max(0, x_coord - 1), min(len(grid), x_coord + 2)):
            for j in range(max(0, y_coord - 1), min(len(grid[0]), y_coord + 2)):
                distance = grid[i][j].calculate_distance(weights)
>>>>>>> fa02d979ac4a7f8cbd08bbad907167fa5b79a9f3
=======
        for i in range(max(0, x_coord - 1), min(len(self.grid), x_coord + 2)):
            for j in range(max(0, y_coord - 1), min(len(self.grid[0]), y_coord + 2)):
                distance = self.grid[i][j].calculate_distance(weights)
>>>>>>> da7317c3b80c6c17b1241f64414b1e0e16a7ed3d
                yield((x_coord, y_coord), distance)


    def calculate_height(self, grid_key, distances):
        distances = list(distances)
        yield(grid_key, sum(distances) / len(distances))


    def steps(self):
<<<<<<< HEAD
<<<<<<< HEAD
        return [MRStep(mapper_init = self.load_weights,
                       mapper = self.calculate_neighborhood,
=======
        return [MRStep(mapper = self.calculate_neighborhood,
>>>>>>> fa02d979ac4a7f8cbd08bbad907167fa5b79a9f3
=======
        return [MRStep(mapper_init = self.load_weights,
                       mapper = self.calculate_neighborhood,
>>>>>>> da7317c3b80c6c17b1241f64414b1e0e16a7ed3d
                       reducer = self.calculate_height)]


if __name__ == "__main__":
    UMatrixMapper.run()