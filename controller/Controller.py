from collections import OrderedDict
from encodings import utf_8


class Controller:
    """Main class in project"""

    def __init__(self, file):
        self.Dict = {}  # Dictionary [key=word:value=count]
        self.file = file
        self.string = None  # string from text.txt
        self.resList = None  # List without dots and etc. and without stopWords
        self.ret = None  # Sorted dictionary D

    def readFile(self):
        """Read strings from text.txt"""
        f = open(self.file, encoding=utf_8.getregentry().name)
        self.string = f.read()
        f.close()

    def writeFile(self):
        """Input results into result.txt"""
        f = open('results.txt', 'w')
        for (key, value) in self.ret:
            f.write('\"{0}\" is {1} times\n'.format(key, value))
        print()
        print('ADDED!')
        print()
        f.close()

    def counter(self):
        """Count amount of words in text"""
        for x in self.resList:
            count = self.resList.count(x)
            self.Dict[x] = count

    def reverseDict(self):
        """Reverse dictionary from up to down"""
        ret = OrderedDict(sorted(self.Dict.items(), key=lambda x: x[0], reverse=False))
        self.ret = sorted(ret.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    '''Test data for Controller.py'''
    I1 = Controller('textfiles\\text.txt')
    I1.readFile()
    I1.counter()
    I1.reverseDict()
