from mrjob.job import MRJob
#from mrjob import protocol
from mrjob.step import MRStep
from SOM import *
import Node

class SOMMapper(MRJob):
    #OUTPUT_PROTOCOL = protocol.TextValueProtocol


    def configure_options(self):
        super(SOMMapper, self).configure_options()
        self.add_passthrough_option("--theta", type = "float")
        self.add_passthrough_option("--n", type = "int")
        self.add_file_option("--map")

    def get_map(self):
        ## Read map from file
        with open(self.options.map) as map_file:
            reader = csv.reader(map_file)
            grid = list(reader)
            for i, row in enumerate(grid):
                for j, node in enumerate(row):
                    weights = [float(x) for x in node[1:-1].split(",")]
                    grid[i][j] = Node.Node(i, j, len(weights), weights)
        return grid

    '''
    def __init__(self, map_weight, args):
        self.map = map_weight
        MRJob.__init__(self, args)
    '''

    def compute_winning_vector(self, input_vector):
        ## Find min distance over K nodes
        grid = self.get_map()

        #print(input_vector)

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
        grid = self.get_map()
        input_vector = [float(x) for x in input_vector.split(",")]
        x, y = self.compute_winning_vector(input_vector)
        ## Accumulate numerator and denominator in weight equation over K nodes
        for i, row in enumerate(grid):
            for j, node in enumerate(row):
                coor_distance = (i - int(x)) ** 2 + (j - int(y)) ** 2

                denominator = math.exp(-coor_distance / self.options.theta ** 2)
                numerator = [denominator * x for x in input_vector]

                #print((numerator, denominator))

                yield((i, j), (numerator, denominator))
        ## accept (GridKey(k), h_ckx, h_ck)


    def accumlate_denominator(self, grid_key, ratios):

        temp = list(ratios)
        #print(len(temp[0]))
        #print(temp[0][0])
        #print(temp[0][1])

        numerator = [0] * self.options.n
        denominator = 0

        for song in temp:
            numerator = list(map(sum, zip(numerator, song[0])))
            denominator = denominator + song[1]

        #grid = self.get_map()
        ## Populate new weight vector by aggregating summations

        #denominator = sum([x[1] for x in ratio])
        ## Update denominator
        #grid[grid_key[0]][grid_key[1]].update_denominator(denominator)
        #yield(grid_key, denominator)


        yield(grid_key, (numerator, denominator))

    def accumulate_numerator(self, grid_key, ratio):
        '''
        grid = self.get_map()
        numerator = list(numerators)
        for x in numerator:
            print(x)
            w = sum(x)
            print(w)
            grid[grid_key[0]][grid_key[1]].update_numerator(w)

        grid[grid_key[0]][grid_key[1]].update_weights()
        '''
        temp = list(ratio)[0]
        '''
        print(type(temp))
        print(temp)
        print(type(temp[0]))
        print(type(temp[1]))
        '''
        weight = [x / temp[1] for x in temp[0]]

        ##print("{} - {}".format(grid_key, weight))

        yield(grid_key, weight)

    def steps(self):
        return [MRStep(mapper = self.accumulate_weights,
                       #combiner = self. ,
                       reducer = self.accumlate_denominator),
                MRStep(reducer = self.accumulate_numerator)
                ]

if __name__ == "__main__":

    SOMMapper.run()