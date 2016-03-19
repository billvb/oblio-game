class OblioAlg(object):
    def __init__(self):
        self.known_tuples = {}

    def put(self, attempted_tuple, response):
        # This is a callback that the oblio engine feeds the results
        # of your guess to.
        self.known_tuples.update({attempted_tuple: response})

    def produce(self):
        raise NotImplemented
