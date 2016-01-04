
import random

from utils import *


class OblioAlg(object):
    def __init__(self):
        self.known_tuples = {}

    def put(self, attempted_tuple, response):
        # This is a callback that the oblio engine feeds the results
        # of your guess to.
        self.known_tuples.update({attempted_tuple: response})

    def produce(self):
        raise NotImplemented


class RandAlg(OblioAlg):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.tuples = [a for a in Utils.yield_all()]
        self.indexes = []

    def produce(self):
        import random
        index = random.randint(0, len(self.tuples) - 1)
        while index in self.indexes:
            index = random.randint(0, len(self.tuples) - 1)
        self.indexes.append(index)
        return self.tuples[index]


class ManualAlg(OblioAlg):
    # This is if you want to play oblio manually.
    def __init__(self):
        super(self.__class__, self).__init__()
        self.tuples = [a for a in Utils.yield_all()]
        self.indexes = []
        self.guesses = []

    def produce(self):
        a, b, c, d = map(lambda a: int(a), raw_input("oblio> ").split(' '))

        guess = OblioTuple((a, b, c, d))
        self.guesses.append(guess)
        return guess
        

class SmartAlg(OblioAlg):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.tuples = [a for a in Utils.yield_all()]
        self.indexes = []
        # Set of possible digits that can be in the solution.
        self.possible_digits = set(range(0, DIGIT_BASE))
        # Mapping table of digits and the likely POSITION within the solution
        # e.g., 2: {0, 3, 4} means that the number 2 can be in tuple position
        # 0, 3, or 4. 
        self.possible_positions = {x: set(range(0, TUPLE_SIZE)) \
            for x in range(0, DIGIT_BASE)}

    def produce(self):
        import random

        if len(self.known_tuples) == 0:
            return OblioTuple((0, 1, 2, 3))
        if len(self.known_tuples) == 1:
            return OblioTuple((1, 2, 3, 4))
        if len(self.known_tuples) == 2:
            return OblioTuple((2, 3, 4, 5))
        if len(self.known_tuples) == 3:
            return OblioTuple((5, 6, 7, 8))

        for guess, response in self.known_tuples.iteritems():
            if response == (0, 0):
                self.possible_digits -= set(guess)
            elif response[0] == TUPLE_SIZE:
                self.possible_digits = set(guess)
            elif response[1] == 0:
                # If we get something in the form of (X, 0), we an eliminate those
                # positional possibilities.
                for x in guess:
                    self.possible_positions[x] -= set([guess.index(x)])

        weights = {x: 1.0 for x in self.possible_digits}
        for guess, response in self.known_tuples.iteritems():
            try:
                if response[0] + response[1] >= 3:
                    for g in guess:
                        weights[g] *= 1.20
                elif response[0] + response[1] <= 1:
                    for g in guess:
                        weights[g] *= 0.80
            except KeyError as e:
                pass

        new_guess = []
        for i in xrange(0, TUPLE_SIZE):
            roll = Utils.weighted_dice_roll(weights, new_guess)
            x = 0
            while i not in self.possible_positions[roll]:
                roll = Utils.weighted_dice_roll(weights, new_guess)
                x += 1
                if x > TUPLE_SIZE * 3:
                    break
            new_guess.append(roll)

        return OblioTuple(tuple(new_guess))


class SmartAlgVariant(OblioAlg):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.tuples = [a for a in Utils.yield_all()]
        self.indexes = []
        # Set of possible digits that can be in the solution.
        self.possible_digits = set(range(0, DIGIT_BASE))
        # Mapping table of digits and the likely POSITION within the solution
        # e.g., 2: {0, 3, 4} means that the number 2 can be in tuple position
        # 0, 3, or 4. 
        self.possible_positions = {x: set(range(0, TUPLE_SIZE)) \
            for x in range(0, DIGIT_BASE)}

    def produce(self):
        import random

        if len(self.known_tuples) == 0:
            return OblioTuple((0, 1, 2, 3))


        for guess, response in self.known_tuples.iteritems():
            if response == (0, 0):
                self.possible_digits -= set(guess)
            elif response[0] == TUPLE_SIZE:
                self.possible_digits = set(guess)
            elif response[1] == 0:
                # If we get something in the form of (X, 0), we an eliminate those
                # positional possibilities.
                for x in guess:
                    self.possible_positions[x] -= set([guess.index(x)])

        weights = {x: 1.0 for x in self.possible_digits}
        for guess, response in self.known_tuples.iteritems():
            try:
                if response[0] + response[1] >= 3:
                    for g in guess:
                        weights[g] *= 1.20
                elif response[0] + response[1] <= 1:
                    for g in guess:
                        weights[g] *= 0.80
            except KeyError as e:
                pass

        new_guess = []
        for i in xrange(0, TUPLE_SIZE):
            roll = Utils.weighted_dice_roll(weights, new_guess)
            x = 0
            while i not in self.possible_positions[roll]:
                roll = Utils.weighted_dice_roll(weights, new_guess)
                x += 1
                if x > TUPLE_SIZE * 3:
                    break
            new_guess.append(roll)

        return OblioTuple(tuple(new_guess))
