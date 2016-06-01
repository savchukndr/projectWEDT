from collections import OrderedDict
from encodings import utf_8


class Controler:
    def __init__(self, file):
        self.Dict = {}
        self.file = file
        self.string = None # string from text.txt
        self.resList = []
        self.ret = None # Dictionary D

    # read from file
    def readFile(self):
        f = open(self.file, encoding=utf_8.getregentry().name)
        self.string = f.read()
        f.close()

    # write into file
    def writeFile(self):
        f = open('results.txt', 'w')
        for (key, value) in self.ret:
            f.write('\"{0}\" is {1} times\n'.format(key, value))
        print()
        print('ADDED!')
        print()
        f.close()

    # counting amount of words in text
    def counter(self):
        for x in self.resList:
            count = self.resList.count(x)
            self.Dict[x] = count

    # reverse dictionary from up to down
    def reverseDict(self):
        ret = OrderedDict(sorted(self.Dict.items(), key=lambda x: x[0], reverse=False))
        self.ret = sorted(ret.items(), key=lambda x: x[1], reverse=True)

if __name__ == '__main__':
    I1 = Controler('textfiles\\text.txt')
    I1.readFile()
    I1.counter()
    I1.reverseDict()
