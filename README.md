# oblio-game

oblio.py: A framework to collect and trade algorithms with your friends to play Oblio.

"Oblio" is a game invented by my high school Computer Science teacher (rules are described below). In our senior year all CS students, as an end-of-semester project, had to produce an algorithm to play it. A tournament was held each year, and the winning students had their names memorialized in the classroom.  As I've personally grown over the years I periodically thought back to this assignment and wondered how well my contemporary self would fare against my high school self.

A long 9-hour AMS-IAD flight equipped with a Macbook Air provided me just the opportunity to dive into this and experiment. Most of the flight was unfortunately spent building this framework, and only a few hours on devising the algorithm. My plan is for this to become a continuous project to enhance and refine my algorithms for whenever I have a few hours to kill on long-haul flights.

Playing Oblio: A talented and trained human averages about 12-15 guesses before converging on the solution. What can your algorithm do?

## To Play Oblio

 1. There exists a secret 4-digit number in which no two digits are the same.
    (e.g., "1 2 3 4" or "0 5 1 2".  "9 9 9 9" is NOT valid)

 2. Whenever you submit a guess of this secret nubmer, you get in return a  2-tuple in the form (X, Y). Y indicates the number of digits within your guess that are in the correct position, and X indicates the number of digits you guessed correctly, but are in the wrong position.

 3. Having the result (0, 4) implies you've won and guessed the secret number correctly.

## Examples

When the secret number is "3 9 4 5":

* If you guess "1 2 4 5", you'll get back (0, 2), because "4" and "5" are in the hidden number, and also in the proper spot.

* If you guess "5 4 9 3", you'll get back (4, 0), as all the digits in your guess are in the hidden number, but none in the correct spot.

* If you guess "0 1 2 8", you'll get back (0, 0). Since none of the digits in your guess are in the secret number.

* If your guess is "2 8 9 1", you'll get back (1, 0), implying you have one correct digit in your guess but it's not in the correct spot. You'll get this a lot and it's annoying.

## Usage

    $ python oblio.py [play|fight|test]

### To play Oblio manually (interactively)

    $ python oblio.py play

### To unit test (pretty minimal)

    $ python oblio.py test

### To fight two algorithms

    $ python oblio.py <AlgClassName> <OtherAlgClassName>

(Ensure both of these exist in the algorithms directory and in the algorithms/__init__.py file)

### To get metrics on random inputs for each algorithm

    $ python metrics.py
    
(Make sure to add yours in the source)
