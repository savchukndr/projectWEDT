class Term:
    def __init__(self, word, sentence):
        self.word = word
        self.sentence = sentence

if __name__ == '__main__':
    I1 = Term('test', 'testSentense')
    print('Word = {0} | Sentense = {1}'.format(I1.word, I1.sentence))