from controler import Controler
from termClass import Term
from sentenceClass import Sentence
from scipy.stats import chisquare as chisq
import numpy as np
import warnings


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
                # Controler.cleanList(self, self.resList)
        self.resListSplit = Group.removeNoneSym(self, self.resList)  # self.resListSplit - with . ! ?
        # print('resListSplit =', self.resListSplit)
        Group.removeStopWords(self)
        return self.resList  # without . ! ?

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
        # print('resListSplitWithDots =', self.resListSplitWithDots)
        resListWithoutDots = list(
            map(lambda x: x[:-1] if x[-1] in ['.', '!', '?', ','] else x, resList))  # Problem with 'jest?'
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
                # self.sentenceList.append(currentSentence)
                # print()
                # print('WORD = {0} | SENTENCE = {1}'.format(currentTerm.word, currentSentence))
                # print('Current Term = ', currentTerm)
                # print()
                continue
            currentTerm = Term(x, currentSentence)
            self.termList.append(currentTerm)
            # print()
            # print('WORD = {0} | SENTENCE = {1}'.format(currentTerm.word, currentSentence))
            # print('Current Term = ', currentTerm)
            # print()

    def remove30percent(self):
        indexToCut = round(len(self.ret) * 0.3)
        self.ret30percent = self.ret[:indexToCut]
        # self.G = {}
        # for (x, y) in self.ret30percent:
        #     self.G[x] = y
        # print('G =', self.G)
        return self.ret30percent

    def converListTuple(self, lst):
        tmp = []
        for (i, j) in lst:
            tmp.append(i)
        return tmp

    def matrixOfApearanceWords(self):
        self.Dw = Group.converListTuple(self, self.ret)
        self.Gw = Group.converListTuple(self, self.ret30percent)
        # print('self.D =', self.D)
        # print('self.G =', self.G)
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
        tmp = self.Dw
        DConv = []
        for z in tmp:
            if len(z) < 20:
                size = 20 - len(z)
                z += ' ' * size
                DConv.append(z)
            elif len(z) > 20:
                size = len(z) - 20
                z = z[:-size]
                DConv.append(z)
            else:
                DConv.append(z)
                continue
        for x in range(len(self.Gw)):
            if x == 0:
                print(' ' * 25, self.Gw[x], end='')
            else:
                print(' ' * 5, self.Gw[x], end='')
        print()
        for z in self.res:
            print(DConv[0], end='')
            for k in z:
                print('      ', k, end='    ')
            DConv = DConv[1:]
            print()

    def formatPowerRes(self, str, symb):
        tmp = ''
        for x in str:
            if x != symb:
                tmp += x
            elif x == symb:
                break
            else:
                continue
        return float(tmp)

    def chiKwadrat(self):
        self.Dc = []
        for (i, j) in self.ret30percent:
            self.Dc.append(j)
        print()
        print('D =', self.res)
        print('Dc =', self.Dc)
        print()
        for x in range(len(self.res)):
            observed = np.array(self.res[x])
            expected = np.array(self.Dc) * np.sum(observed)
            warnings.simplefilter('error', RuntimeWarning) # Filter RuntimeWarning when chi2 called
            try:
                chi2 = str(chisq(observed, expected))
            except RuntimeWarning:
                chi2 = 'Power_divergenceResult(statistic=0, pvalue=0)'
            index = chi2.index(',')
            statistics = Group.formatPowerRes(self, chi2[33:], ',') # Statistics value from Power_divergenceResult (float)
            pvalue = Group.formatPowerRes(self, chi2[index + 9:], ')') # pvalue value from Power_divergenceResult (float)
            print('Statistics = {0} | PValue = {1}'.format(statistics, pvalue))
        print()
        print('scipy.stats.chisquare OUTPUT =', chi2)


if __name__ == '__main__':
    I2 = Group()
    I2.readFromStopWords()
    I2.readFile()
    # print()
    # print('resList = ', I2.splitText())
    I2.splitText()
    # print('D = ', I2.counter())  # MAP dict(without stopwords)
    I2.counter()
    print()
    print('Sorted D =', I2.reverseDict())
    print()
    print('Sorted G = ', I2.remove30percent())
    print()

    # I2.readFromStopWords()
    # I2.readFile()
    # I2.splitText()
    # I2.counter()
    I2.groupSentence()
    I2.matrixOfApearanceWords()
    I2.printMatrix()
    I2.chiKwadrat()
