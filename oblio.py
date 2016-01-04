
import unittest
import random

TUPLE_SIZE = 4
DIGIT_BASE = 10
MAX_GUESS = DIGIT_BASE ** TUPLE_SIZE


class Utils(object):
    @staticmethod
    def yield_all():
        for i in xrange(DIGIT_BASE ** TUPLE_SIZE):
            tup = tuple([int(x) for x in '%04d' % i])
            assert len(tup) == TUPLE_SIZE
            for l in tup:
                if tup.count(l) != 1:
                    break
            else:
                yield OblioTuple(tup)

    @staticmethod
    def weighted_dice_roll(weight_map, exclusions):
        new_map = {k: v for k, v in weight_map.iteritems() if k not in exclusions}
        return new_map.keys()[random.randint(0, len(new_map) - 1)]

class OblioTuple(tuple):
    pass


class OblioContext(object):
   
    def __init__(self, algorithm, hidden_tuple):
        assert isinstance(hidden_tuple, OblioTuple)
        self.algorithm = algorithm
        self.hidden_tuple = hidden_tuple
        self.attempts = 0

    def verify(self, oblio_tuple):
        """Returns (not in correct place, in correct place)"""
        assert isinstance(oblio_tuple, OblioTuple)

        cnt_correct = sum([1 if self.hidden_tuple[i] == oblio_tuple[i] \
            else 0 for i in range(0, TUPLE_SIZE)])
        cnt_misplaced = sum([1 if oblio_tuple[i] in self.hidden_tuple and \
            oblio_tuple[i] != self.hidden_tuple[i] else 0 for i in range(0, TUPLE_SIZE)])

        self.attempts += 1
        return (cnt_misplaced, cnt_correct)

    def solve(self):
        for i in xrange(0, MAX_GUESS):
            guess = self.algorithm.produce()
            response = self.verify(guess)
            if response == (0, TUPLE_SIZE):
                return self.attempts
            else:
                self.algorithm.put(guess, response)
        else:
            raise ValueError("Sucky algorithm")


class OblioAlg(object):
    def __init__(self):
        self.known_tuples = {}

    def put(self, attempted_tuple, response):
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
    def __init__(self):
        super(self.__class__, self).__init__()
        self.tuples = [a for a in Utils.yield_all()]
        self.indexes = []
        self.guesses = []

    def produce(self):
        a, b, c, d = map(lambda a: int(a), raw_input(">>> ").split(' '))

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


class UnitTests(unittest.TestCase):
    def test_verify(self):
        t0 = OblioTuple((0, 1, 2, 3))
        t1 = OblioTuple((3, 2, 1, 0))
        t2 = OblioTuple((6, 7, 8, 9))
        t3 = OblioTuple((3, 1, 8, 9))
        c = OblioContext(OblioTuple((3, 2, 1, 0)))
        self.assertEqual(c.verify(t0), (4, 0))
        self.assertEqual(c.verify(t1), (0, 4))
        self.assertEqual(c.verify(t2), (0, 0))
        self.assertEqual(c.verify(t3), (1, 1))


if __name__ == '__main__':
   # unittest.main()
    
    secrets = [
        (1, 7, 8, 5),
        (2, 1, 9, 7),
        (9, 1, 2, 3),
        (3, 2, 9, 1),
        (0, 8, 2, 1),
        (6, 1, 9, 4),
        (5, 3, 2, 8),
        (2, 7, 4, 3),
        (2, 9, 3, 8)
    ]
    
    alg_dict = {
        SmartAlg: list(),
        RandAlg: list(),
        #ManualAlg: list()
    }

    for a in alg_dict.keys():
        for s in secrets:
            ob = OblioContext(a(), OblioTuple(s))
            alg_dict[a].append(ob.solve())
        print a.__name__, sum(alg_dict[a])/float(len(alg_dict[a]))
