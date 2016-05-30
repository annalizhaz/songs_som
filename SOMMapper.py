from mrjob.job import MRJob
#from mrjob import protocol
from mrjob.step import MRStep
from SOM import *
import Node

class SOMMapper(MRJob):
    #OUTPUT_PROTOCOL = protocol.TextValueProtocol


    def configure_options(self):
        super(SOMMapper, self).configure_options()
        self.add_passthrough_option("--map")

    '''
    def __init__(self, map_weight, args):
        self.map = map_weight
        MRJob.__init__(self, args)
    '''

    def compute_winning_vector(self, input_vector):
        ## Find min distance over K nodes
        print(type(self.options.map))
        min_distance = self.options.map[0][0].calculate_distance(input_vector)
        bmu = (0, 0)
        for i, row in enumerate(self.options.map):
            for j, node in enumerate(row):
                distance = node.calculate_distance(input_vector)
                ## Update best matching unit
                if min_distance > distance:
                    min_distance = distance
                    bmu = (i, j)
        return bmu

    def accumulate_weights(self, _, input_vector):
        bum = self.compute_winning_vector(input_vector)
        ## Accumulate numerator and denominator in weight equation over K nodes
        for i, row in enumerate(self.option.map):
            for j, node in enumerate(row):
                coor_distance = (i - bmu[0])^2 + (j - bmu[1]) ** 2
                denominator = math.exp(-coor_distance / theta ** 2)
                numerator = [denominator * x for x in input_vector]

                yield((i, j), (numerator, denominator))
        ## accept (GridKey(k), h_ckx, h_ck)


    def accumlate_denominator(self, grid_key, ratios):
        ## Populate new weight vector by aggregating summations
        ratio = list(ratios)
        denominator = sum([x[1] for x in ratio])
        ## Update denominator
        self.options.map[grid_key[0]][grid_key[1]].update_denominator(denominator)
        #yield(grid_key, denominator)

        for value in ratio:
            yield(grid_key, ratio[0])

    def accumulate_numerator(self, grid_key, numerators):
        numerator = list(numerators)
        for x in numerator:
            self.options.map[grid_key[0]][grid_key[1]].update_numerator(x)

        self.options.map[grid_key[0]][grid_key[1]].update_weights()


    def steps(self):
        return [MRStep(mapper = self.accumulate_weights,
                       #combiner = self. ,
                       reducer = self.accumlate_denominator),
                MRStep(reducer = self.accumulate_numerator)]

if __name__ == "__main__":

    SOMMapper.run()