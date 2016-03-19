"""

oblio.py: A framework to collect and trade algorithms with your friends to play Oblio.

A talented and trained human get average
about 12-15 guesses before converging on the solution. What can your algorithm
do?

To play Oblio:

    - There exists a secret 4-digit number in which no two digits are the same.
      (e.g., "1 2 3 4" or "0 5 1 2".  "9 9 9 9" is NOT valid)

    - Whenever you submit a guess of this secret nubmer, you get in return a 
      2-tuple in the form (X, Y). Y indicates the number of digits within
      your guess that are in the correct position, and X indicates the number
      of digits you guessed correctly, but are in the wrong position.

    - Having the result (0, 4) implies you've won and guessed the secret number
      correctly.

EXAMPLES:

    When the secret number is "3 9 4 5":

    - If you guess "1 2 4 5", you'll get back (0, 2), because "4" and "5" are
      in the hidden number, and also in the proper spot.

    - If you guess "5 4 9 3", you'll get back (4, 0), as all the digits in 
      your guess are in the hidden number, but none in the correct spot.

    - If you guess "0 1 2 8", you'll get back (0, 0). Since none of the digits 
      in your guess are in the secret number.

    - If your guess is "2 8 9 1", you'll get back (1, 0), implying you have
      one correct digit in your guess but it's not in the correct spot. You'll
      get this a lot and it's annoying.


"""

from __future__ import print_function
import sys
import unittest
import random
import json

from algorithms.utils import OblioTuple
from algorithms.utils import MAX_GUESS
from algorithms.utils import TUPLE_SIZE
from algorithms.utils import DIGIT_BASE

import algorithms

__credits__ = ["beer", "no internet access", "9 hour long-haul flight"]


class OblioContext(object):
    """ Represents an oblio engine that is holding the secret number """

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

    def solve(self, print_response=False):
        for i in xrange(0, MAX_GUESS):
            guess = self.algorithm.produce()
            response = self.verify(guess)
            if response == (0, TUPLE_SIZE):
                return self.attempts
            else:
                if print_response:
                    print('Guess %3d: %s --> %s' % (i, guess, response))
                self.algorithm.put(guess, response)
        else:
            # There are fewer than 10,000 possibilities,
            # so if your algorithm cannot get the correct solution
            # in 10,000 tries, you[r solution] sucks.
            raise ValueError("Sucky algorithm")


class UnitTests(unittest.TestCase):
    def test_verify(self):
        t0 = OblioTuple((0, 1, 2, 3))
        t1 = OblioTuple((3, 2, 1, 0))
        t2 = OblioTuple((6, 7, 8, 9))
        t3 = OblioTuple((3, 1, 8, 9))
        c = OblioContext(None, OblioTuple((3, 2, 1, 0)))
        self.assertEqual(c.verify(t0), (4, 0))
        self.assertEqual(c.verify(t1), (0, 4))
        self.assertEqual(c.verify(t2), (0, 0))
        self.assertEqual(c.verify(t3), (1, 1))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Play Oblio')
    parser.add_argument('subcommand', type=str, nargs='+',
        help='play, test, or fight')

    args = parser.parse_args()

    if args.subcommand[0] == 'play':
        secret_tuple = OblioTuple.get_random()
        context = OblioContext(algorithms.ManualAlg(), secret_tuple)
        context.solve(print_response=True)
    elif args.subcommand[0] == 'test':
        suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
        unittest.TextTestRunner(verbosity=2).run(suite)
    elif args.subcommand[0] == 'fight':
        ngames = 100
        alg1, alg2 = args.subcommand[1:]
        l_contender = getattr(algorithms, alg1)
        r_contender = getattr(algorithms, alg2)

        l_wins, r_wins = 0, 0
        for game_cnt in xrange(0, ngames):
            secret_tuple = OblioTuple.get_random()
            l_cnt = OblioContext(l_contender(), secret_tuple).solve()
            r_cnt = OblioContext(r_contender(), secret_tuple).solve()
            
            if l_cnt < r_cnt:
                l_wins += 1
            elif l_cnt > r_cnt:
                r_wins += 1

        winner, margin = (l_contender, float(l_wins)/game_cnt) \
            if l_wins > r_wins else (r_contender, float(r_wins)/game_cnt)
        
        print(json.dumps({'winner': str(winner), 'margin': '%2.1f' % (margin * 100)},
            indent=4))
        
    else:
        print('Unknown subcommand: ', args.subcommand, file=sys.stderr)
        sys.exit(1)
