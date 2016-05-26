from controler import Controler
from termClass import Term
from sentenceClass import Sentence

class Group(Controler):
    def __init__(self):
        Controler.__init__(self, file='text.txt')

    def readFromStopWords(self, file='stopwords.txt'):
        f = open(file).read()
        stopWordsList = f.split(' ')
        self.stopWordsList = []
        for x in stopWordsList:
            self.stopWordsList.append(u'{0}'.format(x[:-1]))
        return self.stopWordsList

    def splitText(self):
        self.string = self.string.lower()
        self.listNsplit = self.string.split('\n')
        self.resList = []
        for i in self.listNsplit:
            tmp = i.split(' ')
            for j in tmp:
                self.resList.append(j)
            #Controler.cleanList(self, self.resList)
        self.resListSplit = Group.removeNoneSym(self, self.resList) #self.resListSplit - with . ! ?
        print('resListSplit =', self.resListSplit)
        Group.removeStopWords(self)
        return self.resList #without . ! ?

    def removeNoneSym(self, lst):
        tmp = []
        for x in lst:
            if not x:
                continue
            else:
                tmp.append(x)
        return tmp

    def removeStopWords(self):
        tmp = Group.removeNoneSym(self, self.resList)
        resList = []
        for x in tmp:
            if x[-1] in ['.', '!', '?'] and x[:-1] in self.stopWordsList:
                x = 'termword' + x[-1]
            if x in self.stopWordsList:
                continue
            else:
                resList.append(x)
        self.resListSplitWithDots = resList
        print('resListSplitWithDots =', self.resListSplitWithDots)
        resListWithoutDots = list(map(lambda x: x[:-1] if x[-1] in ['.', '!', '?'] else x, resList)) #Problem with 'jest?'
        self.resList = []
        self.resList = resListWithoutDots
        return self.resList

    def groupSentence(self):
        sentenceStart = True
        self.sentenceList = []
        self.termList = []
        for x in self.resListSplitWithDots:
            if sentenceStart:
                currentSentence = Sentence()
                sentenceStart = False
            if x.endswith('.') or x.endswith('!') or x.endswith('?'):
                if x[:-1] == 'termword':
                    sentenceStart = True
                    continue
                x = x[:-1]
                sentenceStart = True
                currentTerm = Term(x, currentSentence)
                self.termList.append(currentTerm)
                self.sentenceList.append(currentSentence)
                print()
                print('WORD = {0} | SENTENCE = {1}'.format(currentTerm.word, currentSentence))
                print('Current Term = ', currentTerm)
                print()
                continue
            currentTerm = Term(x, currentSentence)
            self.termList.append(currentTerm)
            print()
            print('WORD = {0} | SENTENCE = {1}'.format(currentTerm.word, currentSentence))
            print('Current Term = ', currentTerm)
            print()

    def remove30percent(self):
        indexToCut = round(len(self.ret) * 0.3)
        self.ret30percent = self.ret[:indexToCut]
        self.G = {}
        for (x, y) in self.ret30percent:
            self.G[x] = y
        print('G =', self.G)
        return self.ret30percent

    def matrixOfApearanceWords(self):
        self.D = {}
        self.tmp = {}
        print('sentence LIST =', self.sentenceList)
        print('term LIST =', self.termList)
        for (i, j) in self.ret:
            for (k, l) in self.ret30percent:
                for x in self.sentenceList:
                    print()
                    print('s e n t e n c e =', x)
                    print()
                    for y in self.termList:
                        print('t e r m w o r d =', y)
                        if i == y.word:
                            curSen = y.sentence
                            if x == curSen:
                                if i == k:
                                    self.tmp[k] = 0
                                else:
                                    self.tmp[k] = 'ok'
                    self.D[i] = self.tmp
                            #self.tmp[y.word] = y.sentence
        print('TMP =', self.tmp)
        print('D =', self.D)
                #for (i, j) in self.ret:
                    #for (l, m) in self.ret30percent:


            #for y in self.sentenceList:
                #print(y)
                #for x in y:
                    #k = x.sentence
                #print(y)
                    #print('Word = {0} | Sentence = {1}'.format(x.word, x.sentence))
                    #if i == x.word and x.sentence == k:
                    #    print('ok ', x.word)
                    #else:
                    #    print('ne ok', x.word)


    def printMatrix(self):
        for key in self.D.keys():
            print("%10s " % key)
            for k in self.D.values():
                for ky in k:
                    print(k[ky], end=' ')
            print()


if __name__ == '__main__':
    I2 = Group()
    I2.readFromStopWords()
    I2.readFile()
    print()
    print('resList = ', I2.splitText())
    print('D = ', I2.counter()) #MAP dict(without stopwords)
    print('Sorted D =', I2.reverseDict())
    print()

    print('Sorted G = ',I2.remove30percent())

    #I2.readFromStopWords()
    #I2.readFile()
    #I2.splitText()
    #I2.counter()
    I2.groupSentence()
    I2.matrixOfApearanceWords()
    I2.printMatrix()