import json

from oblio import OblioContext

from algorithms.utils import OblioTuple
from algorithms.utils import MAX_GUESS
from algorithms.utils import TUPLE_SIZE
from algorithms.utils import DIGIT_BASE

import algorithms

if __name__ == '__main__':
    #unittest.main()
    
    secrets = [
        (1, 7, 8, 5),
        (2, 1, 9, 7),
        (9, 1, 2, 3),
        (3, 2, 9, 1),
        (0, 8, 2, 1),
        (6, 1, 9, 4),
        (5, 3, 2, 8),
        (2, 7, 4, 3),
        (2, 9, 3, 8),
        (6, 3, 2, 0),
        (0, 1, 2, 9),
        (0, 1, 9, 4),
        (4, 9, 0, 8),
        (1, 9, 2, 8),
        (7, 6, 5, 0),
        (4, 3, 0, 1),
        (4, 1, 8, 2),
        (0, 2, 4, 3),
        (3, 5, 2, 4),
        (1, 2, 9, 3),
        (3, 4, 5, 6),
        (1, 4, 7, 2)
    ]
   
    # You can plug in your algorithm here.
    alg_dict = {
        algorithms.SmartAlg: list(),
        algorithms.SmartAlgVariant: list(),
        algorithms.RandAlg: list(),
    }

    for a in alg_dict.keys():
        for s in secrets:
            ob = OblioContext(a(), OblioTuple(s))
            alg_dict[a].append(ob.solve())
        print json.dumps({
            'name': a.__name__,
            'mean': sum(alg_dict[a])/float(len(alg_dict[a])),
            'median': sorted(alg_dict[a])[len(alg_dict[a])/2] },
            indent=4)
