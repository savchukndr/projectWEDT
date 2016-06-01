class Term:
    """Class Term"""

    LAST_ID = -1

    def __init__(self, word, sentence):
        self.word = word
        self.sentence = sentence
        Term.LAST_ID += 1
        self.id = Term.LAST_ID

    def __str__(self, *args, **kwargs):
        return self.__repr__(args, kwargs)

    def __repr__(self, *args, **kwargs):
        return "Term#{0!r}={1!r}".format(self.id, self.word)


if __name__ == '__main__':
    """Test data for termClass.py"""
    I1 = Term('test', 'testSentense')
    print('Word = {0} | Sentense = {1}'.format(I1.word, I1.sentence))
