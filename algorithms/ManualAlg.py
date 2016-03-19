
from OblioAlg import OblioAlg
import utils
from utils import OblioTuple

class ManualAlg(OblioAlg):
    # This is if you want to play oblio manually.
    def __init__(self):
        super(self.__class__, self).__init__()
        self.tuples = [a for a in utils.yield_all()]
        self.indexes = []
        self.guesses = []

    def produce(self):
        a, b, c, d = map(lambda a: int(a), raw_input("oblio> ").split(' '))

        guess = OblioTuple((a, b, c, d))
        self.guesses.append(guess)
        return guess
