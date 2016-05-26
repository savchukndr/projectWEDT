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

    def converListTuple(self, lst):
        tmp = []
        for (i, j) in lst:
            tmp.append(i)
        return tmp

    def matrixOfApearanceWords(self):
        D = Group.converListTuple(self, self.ret)
        G = Group.converListTuple(self, self.ret30percent)
        tmp = []
        res = []
        # print('sentence LIST =', self.sentenceList)
        # print('term LIST =', self.termList)
        for i in range(len(D)):
            listSenD = []
            for z in self.termList:
                if D[i] == z.word:
                    listSenD.append(z.sentence)
            listSenDSet = list(set(listSenD))
            for k in range(len(G)):
                count = 0
                for y in self.termList:
                    if y.sentence in listSenDSet:
                        if y.word == D[i] and y.word == G[k]:
                            break
                        elif y.word == G[k]:
                            count += 1
                        else:
                            continue
                tmp.append(count)
            res.append(tmp)
            tmp = []
        print('TMP =', tmp)
        print('D =', res)


    def printMatrix(self):
        for key in self.D.keys():
            print("%10s " % key)
            for k in self.D.values():
                for ky in k:
                    print(k[ky], end=' ')
                break
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