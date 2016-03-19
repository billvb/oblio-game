from OblioAlg import OblioAlg
import utils

class RandAlg(OblioAlg):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.tuples = [a for a in utils.yield_all()]
        self.indexes = []

    def produce(self):
        import random
        index = random.randint(0, len(self.tuples) - 1)
        while index in self.indexes:
            index = random.randint(0, len(self.tuples) - 1)
        self.indexes.append(index)
        return self.tuples[index]
        


