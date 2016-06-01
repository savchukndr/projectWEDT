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
    '''Class Group '''
    def __init__(self):
        Controler.__init__(self, file='textfiles\\text.txt')
        self.resList = None  # List without dots and etc. and without stopWords
        self.stopWordsList = None # StopWord list
        self.resListSplit = None # List with dots and etc. and with stopWords
        self.sentenceList = [] # Sentence list
        self.termList = [] # Term list
        self.ret30percent = None # Dictionary G
        self.resListSplitWithDots = None # List with dots and etc.
        self.Dw = None # Dw = ['konczy', 'sie', 'zdanie'] from D = [('konczy', 2), ('sie', 2), ('zdanie', 2)]
        self.Gw = None # Thesame like Dw
        self.res = None # Matrix

    def readFromStopWords(self, file='textfiles\stopwords.txt'):
        """Reading words from stopwords.txt"""
        f = open(file, encoding=utf_8.getregentry().name)
        self.stopWordsList = f.read().split('\n')
        f.close()

    def splitText(self):
        """Split string, for separated words"""
        string = self.string.lower()
        self.resList = string.split()
        self.resListSplit = Group.removeNoneSym(self.resList)
        Group.removeStopWords(self)

    @staticmethod
    def removeNoneSym(lst):
        """Remove None symbols from list"""
        tmp = []
        for x in lst:
            if not x:
                continue
            else:
                tmp.append(x)
        return tmp

    def removeStopWords(self):
        """Remove StopWords from list"""
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
        """Devide words for terms and then for sentences"""
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
        """Create map G == 30% from D"""
        indexToCut = round(len(self.ret) * 0.3)
        self.ret30percent = self.ret[:indexToCut]

    @staticmethod
    def converListTuple(lst):
        """Converting list [('word1', count1),('word2': count2), ...] into ['word1', 'word2']"""
        tmp = []
        for (i, j) in lst:
            tmp.append(i)
        return tmp

    def matrixOfApearanceWords(self):
        """Creating matrix"""
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
        """Output matrix"""
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
        """Chi-square function"""
        Dc = [] # Dc = [2, 2, 2] from D = [('konczy', 2), ('sie', 2), ('zdanie', 2)]
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
        """Jensen-Shannon divergence"""
        _P = P / norm(P, ord=1)
        _Q = Q / norm(Q, ord=1)
        _M = 0.5 * (_P + _Q)
        res = 0.5 * (entropy(_P, _M) + entropy(_Q, _M))
        return res

    def outPutJSDval(self):
        """Output Jensen-Shannon divergence function results"""
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
    """Test data for groupClass.py"""
    I2 = Group()
    I2.readFromStopWords()
    I2.readFile()
    I2.splitText()
    I2.counter()
    print()
    I2.reverseDict()
    print('Sorted D =', I2.ret)
    print()
    I2.remove30percent()
    print('Sorted G = ', I2.ret30percent)
    print()
    I2.groupSentence()
    I2.matrixOfApearanceWords()
    I2.printMatrix()
    I2.chiKwadrat()
    I2.outPutJSDval()
