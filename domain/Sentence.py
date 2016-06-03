class Sentence:
    """Class Sentence"""

    LAST_ID = -1

    def __init__(self):
        self.termList = []
        Sentence.LAST_ID += 1
        self.id = Sentence.LAST_ID

    def __str__(self, *args, **kwargs):
        return self.__repr__(args, kwargs)

    def __repr__(self, *args, **kwargs):
        return "Sentence#{0!r}={1!r}".format(self.id, self.termList)
