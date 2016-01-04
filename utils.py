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
        # Actually, this does an UNWEIGHTED dice roll. Never got around to doing weighted.
        # Don't think it would matter much anyway.
        new_map = {k: v for k, v in weight_map.iteritems() if k not in exclusions}
        return new_map.keys()[random.randint(0, len(new_map) - 1)]


class OblioTuple(tuple):
    # This is probably un-necessary.
    pass


