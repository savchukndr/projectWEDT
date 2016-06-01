class Sentence:
    """Class Sentence"""

    LAST_ID = -1

    def __init__(self):
        self.sentenceList = []
        Sentence.LAST_ID += 1
        self.id = Sentence.LAST_ID

    def __str__(self, *args, **kwargs):
        return self.__repr__(args, kwargs)

    def __repr__(self, *args, **kwargs):
        return "Sentence#{0!r}={1!r}".format(self.id, self.sentenceList)


if __name__ == '__main__':
    """Test data for sentenceClass.py"""
    I1 = Sentence()
    I1.termList = [1, 2, 3]
    print('Term List =', I1.sentenceList)
