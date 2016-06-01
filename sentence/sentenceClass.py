class Sentence:
    '''Class Sentence'''
    def __int__(self):
        self.sentenceList = []


if __name__ == '__main__':
    """Test data for sentenceClass.py"""
    I1 = Sentence()
    I1.termList = [1, 2, 3]
    print('Term List =', I1.sentenceList)
