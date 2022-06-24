class Action:
    def __init__(self, sample):
        location, connection = tuple(sample[:-1]), sample[-1]
        self.location = location
        self.connection = connection