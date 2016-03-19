import random

TUPLE_SIZE = 4
DIGIT_BASE = 10
MAX_GUESS = DIGIT_BASE ** TUPLE_SIZE


def yield_all():
    for i in xrange(DIGIT_BASE ** TUPLE_SIZE):
        tup = tuple([int(x) for x in '%04d' % i])
        assert len(tup) == TUPLE_SIZE
        for l in tup:
            if tup.count(l) != 1:
                break
        else:
            yield OblioTuple(tup)

def weighted_dice_roll(weight_map, exclusions):
    # Actually, this does an UNWEIGHTED dice roll. Never got around to doing weighted.
    # Don't think it would matter much anyway.
    new_map = {k: v for k, v in weight_map.iteritems() if k not in exclusions}
    return new_map.keys()[random.randint(0, len(new_map) - 1)]

class OblioTuple(tuple):
    @staticmethod
    def get_random():
        pile = range(0, DIGIT_BASE)
        secret = []
        for i in xrange(0, TUPLE_SIZE):
            r = random.randint(0, len(pile) - 1)
            secret.append(pile[r])
            del pile[r]

        # Assert that the tuple contains 4 distinct digits
        assert len(list(set(secret))) == 4

        return OblioTuple(secret)
