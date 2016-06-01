import warnings
from encodings import utf_8

import numpy as np
from numpy.linalg import norm
from scipy.stats import chisquare as chisq
from scipy.stats import entropy
from controler import Controler
from sentence.sentenceClass import Sentence
from sentence.termClass import Term


class Group(Controler):
    def __init__(self):
        Controler.__init__(self, file='textfiles\\text.txt')
        self.resList = None  # co to jest
        self.stopWordsList = None
        self.resListSplit = None
        self.sentenceList = []
        self.termList = []
        self.ret30percent = None # Dictionary G
        self.resListSplitWithDots = None # List with dots and etc.
        self.Dw = None # Dw = [2, 2, 2, 1, 1] from D = [('konczy', 2), ('sie', 2), ('zdanie', 2), ('drugie', 1), ('pierwsze', 1), ('zzz', 1)]
        self.Gw = None
        self.res = None

    def readFromStopWords(self, file='textfiles\stopwords.txt'):
        f = open(file, encoding=utf_8.getregentry().name)
        self.stopWordsList = f.read().split('\n')
        f.close()
        return self.stopWordsList

    def splitText(self):
        string = self.string.lower()
        self.resList= string.split()
        self.resListSplit = Group.removeNoneSym(self.resList)
        Group.removeStopWords(self)
        print('resList =', self.resList)

    @staticmethod
    def removeNoneSym(lst):
        tmp = []
        for x in lst:
            if not x:
                continue
            else:
                tmp.append(x)
        return tmp

    def removeStopWords(self):
        tmp = Group.removeNoneSym(self.resList)
        resList = []
        for x in tmp:
            if x[-1] in ['.', '!', '?'] and x[:-1] in self.stopWordsList:
                resList[-1] += x[-1]
            elif x in self.stopWordsList:
                continue
            else:
                resList.append(x)
        self.resListSplitWithDots = resList
        resListWithoutDots = list(map(lambda x: x[:-1] if x[-1] in ['.', '!', '?', ','] else x, resList))
        self.resList = resListWithoutDots

    def groupSentence(self):
        sentenceStart = True
        for x in self.resListSplitWithDots:
            if sentenceStart:
                currentSentence = Sentence()
                sentenceStart = False
            if x.endswith('.') or x.endswith('!') or x.endswith('?'):
                x = x[:-1]
                sentenceStart = True
                currentTerm = Term(x, currentSentence)
                self.termList.append(currentTerm)
                continue
            currentTerm = Term(x, currentSentence)
            self.termList.append(currentTerm)

    def remove30percent(self):
        indexToCut = round(len(self.ret) * 0.3)
        self.ret30percent = self.ret[:indexToCut]

    @staticmethod
    def converListTuple(lst):
        tmp = []
        for (i, j) in lst:
            tmp.append(i)
        return tmp

    def matrixOfApearanceWords(self):
        self.Dw = Group.converListTuple(self.ret)
        self.Gw = Group.converListTuple(self.ret30percent)
        tmp = []
        self.res = []
        for i in range(len(self.Dw)):
            listSenD = []
            for z in self.termList:
                if self.Dw[i] == z.word:
                    listSenD.append(z.sentence)
            listSenDSet = list(set(listSenD))
            for k in range(len(self.Gw)):
                count = 0
                for y in self.termList:
                    if y.sentence in listSenDSet:
                        if y.word == self.Dw[i] and y.word == self.Gw[k]:
                            break
                        elif y.word == self.Gw[k]:
                            count += 1
                        else:
                            continue
                tmp.append(count)
            self.res.append(tmp)
            tmp = []

    def printMatrix(self):
        firstColumnWidth = 25
        cellWidth = 10
        firstColumnFormat = '{0:' + str(firstColumnWidth) + '.' + str(firstColumnWidth) + 's}'
        cellFormat = ' {0:' + str(cellWidth) + '.' + str(cellWidth) + 's}'

        # matrix header
        print(firstColumnFormat.format(''), end='')
        for x in range(len(self.Gw)):
            print(cellFormat.format(self.Gw[x]), end='')
        print()  # new line

        # matrix body
        for i in range(len(self.Dw)):
            print(firstColumnFormat.format(self.Dw[i]), end='')
            row = self.res[i]
            for cell in row:
                print(cellFormat.format(str(cell)), end='')
            print()

    def chiKwadrat(self):
        Dc = []
        for (i, j) in self.ret30percent:
            Dc.append(j)
        print()
        print('D =', self.res)
        print('Dc =', Dc)
        print()
        for x in range(len(self.res)):
            observed = np.array(self.res[x])
            expected = np.array([1 / len(Dc)] * len(Dc)) * np.sum(observed)
            warnings.simplefilter('error', RuntimeWarning)  # Filter RuntimeWarning when chi2 called
            try:
                chi2 = chisq(observed, expected)
                print('Statistics = {0} | PValue = {1}'.format(chi2.statistic, chi2.pvalue))
            except RuntimeWarning:
                print('Statistics = {0} | PValue = {1}'.format(0, 0))
        print()

    @staticmethod
    def JSD(P, Q):
        _P = P / norm(P, ord=1)
        _Q = Q / norm(Q, ord=1)
        _M = 0.5 * (_P + _Q)
        res = 0.5 * (entropy(_P, _M) + entropy(_Q, _M))
        return res

    def outPutJSDval(self):
        countStep = 0
        tmp = self.res
        for x in self.res:
            if sum(x) == 0:
                res = 0
                countStep += 1
                print('step = ', countStep)
                print(res)
                continue
            else:
                tmp = tmp[1:]
                for y in tmp:
                    if sum(y) == 0:
                        res = 0
                        countStep += 1
                        print('step = ', countStep)
                        print(res)
                        continue
                    else:
                        res = Group.JSD(x, y)
                        countStep += 1
                        print('step = ', countStep)
                        print(res)


if __name__ == '__main__':
    I2 = Group()
    I2.readFromStopWords()
    I2.readFile()
    I2.splitText()
    I2.counter()
    print()
    print('Sorted D =', I2.reverseDict())
    print()
    I2.remove30percent()
    print('Sorted G = ', I2.ret30percent)
    print()
    I2.groupSentence()
    I2.matrixOfApearanceWords()
    I2.printMatrix()
    I2.chiKwadrat()
    I2.outPutJSDval()
