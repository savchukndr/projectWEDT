import subprocess
from encodings import utf_8

from nltk.stem.porter import PorterStemmer
from numpy.linalg import norm
from scipy.stats import entropy

from controler import Controler
from domain.Sentence import Sentence
from domain.Term import Term


class Group(Controler):
    """Class Group"""

    def __init__(self, language='pl'):
        Controler.__init__(self, file='textfiles\\text.txt')
        self.language = language
        self.special_characters = ['.', '!', '?', ',', '"', '\'', ')', '(', '-', '–', ':', ';']
        self.end_of_sentence_characters = ['.', '!', '?']
        self.resList = None  # List without dots and etc. and without stopWords
        self.stopWordsList = None  # StopWord list
        self.resListSplit = None  # List with dots and etc. and with stopWords
        self.sentenceList = []  # Sentence list
        self.termList = []  # Term list
        self.ret30percent = None  # Dictionary G
        self.resListSplitWithDots = None  # List with dots and etc.
        self.Dw = None  # Dw = ['konczy', 'sie', 'zdanie'] from D = [('konczy', 2), ('sie', 2), ('zdanie', 2)]
        self.Gw = None  # Thesame like Dw
        self.wordTermDict = {}  # dictionary [word:(term1, term2, ...)]
        self.coocurenceMatrix = None  # Matrix
        self.termSentencesTotalSize = []  # counts all terms in sentence where a term occurs
        self.chi2Values = []  # list of tuples (word, values of chi squared)
        self.porterStemmer = PorterStemmer()  # stemmer for english
        self.morfeuszProcess = subprocess.Popen(['morfeusz_bin\morfeusz_analyzer.exe', '-c', 'UTF8'],
                                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                bufsize=1)

    def readFromStopWords(self):
        """Reading words from stopwords.txt"""
        file = 'textfiles\polish_stopwords.txt' if self.language == 'pl' else 'textfiles\english_stopwords.txt'
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
            if x[-1] in self.end_of_sentence_characters and x[:-1] in self.stopWordsList:
                if len(resList) > 0:
                    resList[-1] += x[-1]
            elif x in self.stopWordsList or x in self.special_characters:
                continue
            else:
                prefix = ''
                suffix = ''
                while len(x) >= 1 and x[0] in self.special_characters:
                    prefix += x[0]
                    x = x[1:]
                while len(x) >= 1 and x[-1] in self.special_characters:
                    suffix = x[-1] + suffix
                    x = x[:-1]
                x_stemmed = self.stemAWord(x)
                x_stemmed = prefix + x_stemmed + suffix  # restore special characters for sentence end retrieving
                resList.append(x_stemmed)

        self.resListSplitWithDots = resList

        # remove special characters
        self.resList = []
        for word in resList:
            while len(word) >= 1 and word[0] in self.special_characters:
                word = word[1:]
            while len(word) >= 1 and word[-1] in self.special_characters:
                word = word[:-1]
            self.resList.append(word)

    def stemAWord(self, x: str):
        if self.language == 'pl':
            self.morfeuszProcess.stdin.write(utf_8.encode(x + "\n")[0])
            self.morfeuszProcess.stdin.flush()

            readBytes = self.morfeuszProcess.stdout.readline()
            line = utf_8.decode(readBytes, errors='ignore')[0]
            morfeuszInputAssumption = line.split(',')[2].split(':')[0]
            if morfeuszInputAssumption != x:
                # pominięcie wyników z tej samej sekcji
                while not (line.endswith(']\r') or line.endswith(']\n') or line.endswith(']\r\n') or line.endswith(']\n\r')):
                    readBytes = self.morfeuszProcess.stdout.readline()
                    line = utf_8.decode(readBytes, errors='ignore')[0]
                # hack np. na wyraz "gdybym", "czym", który dostaje 2 outputy
                readBytes = self.morfeuszProcess.stdout.readline()
                line = utf_8.decode(readBytes, errors='ignore')[0]
                morfeuszInputAssumption = line.split(',')[2].split(':')[0]
                if morfeuszInputAssumption != x:
                    return x

            stemmed = line.split(',')[3].split(':')[0]  # bierzemy tylko pierwszy wynik z listy
            while not (line.endswith(']\r') or line.endswith(']\n') or line.endswith(']\r\n') or line.endswith(']\n\r')):
                readBytes = self.morfeuszProcess.stdout.readline()
                line = utf_8.decode(readBytes, errors='ignore')[0]
            print("STEM {0:10.10s} -> {1:10.10s}".format(x, stemmed))
            return stemmed
        else:
            return self.porterStemmer.stem(x)

    def groupSentence(self):
        """Divide words for terms and then for sentences"""
        sentenceStart = True
        currentSentence = None
        for x in self.resListSplitWithDots:
            if sentenceStart:
                currentSentence = Sentence()
                sentenceStart = False
            if x[-1] in self.end_of_sentence_characters:
                x = x[:-1]
                sentenceStart = True
            while len(x) >= 1 and x[0] in self.special_characters:
                x = x[1:]
            while len(x) >= 1 and x[-1] in self.special_characters:
                x = x[:-1]
            currentTerm = Term(x, currentSentence)
            currentSentence.termList.append(currentTerm)
            self.termList.append(currentTerm)

            # filling wordTermDict
            if self.wordTermDict.get(currentTerm.word) is None:
                self.wordTermDict[currentTerm.word] = []
            self.wordTermDict[currentTerm.word].append(currentTerm)

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
        wordToIdxDict = {}
        for i in range(len(self.ret)):
            wordToIdxDict[self.ret[i][0]] = i
        # noinspection PyUnusedLocal
        self.coocurenceMatrix = [[0 for x in range(len(self.Gw))] for y in range(len(self.Dw))]
        # noinspection PyUnusedLocal
        self.termSentencesTotalSize = [0 for x in range(len(self.Dw))]
        for w_idx in range(len(self.Dw)):
            w = self.Dw[w_idx]
            for wTerm in self.wordTermDict[w]:  # dla wszystkich termów odpowiadających 'w'
                self.termSentencesTotalSize[w_idx] += len(wTerm.sentence.termList)
                for sameSentenceTerm in wTerm.sentence.termList:
                    g_idx = wordToIdxDict[sameSentenceTerm.word]
                    if sameSentenceTerm.word != wTerm.word and g_idx < len(self.Gw):
                        self.coocurenceMatrix[w_idx][g_idx] += 1
        print(self.termSentencesTotalSize)

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
            row = self.coocurenceMatrix[i]
            for cell in row:
                print(cellFormat.format(str(cell)), end='')
            print()

    def chiKwadrat(self):
        """Custom chi-square function, as in article"""
        Dc = []  # Dc = [2, 2, 2] from D = [('konczy', 2), ('sie', 2), ('zdanie', 2)]
        for (i, j) in self.ret30percent:
            Dc.append(j)
        print()
        print('D =', self.coocurenceMatrix)
        print('Dc =', Dc)
        print()
        # noinspection PyUnusedLocal
        for w_idx in range(len(self.coocurenceMatrix)):
            w = self.coocurenceMatrix[w_idx]
            chi2Value = 0
            chi2MaxComponent = 0
            for g_idx in range(len(w)):
                fwg = w[g_idx]  # freq(w, g), liczba współwystępowań słów w i g w zdaniach

                nwpg = self.termSentencesTotalSize[w_idx] * self.termSentencesTotalSize[g_idx] / len(self.termList)
                chi2Component = ((fwg - nwpg) ** 2) / nwpg
                chi2Value += chi2Component
                if chi2Component > chi2MaxComponent:
                    chi2MaxComponent = chi2Component
            chi2Value -= chi2MaxComponent
            self.chi2Values.append((self.ret[w_idx][0], chi2Value))
        print()
        self.chi2Values.sort(key=lambda x: x[1], reverse=True)
        print(self.chi2Values)

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
        tmp = self.coocurenceMatrix
        for x in self.coocurenceMatrix:
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

    def printResults(self):
        print("=" * 80)
        print("Słowa kluczowe:")
        print("=" * 80)
        for i in range(20):
            print("{0:3d}. {1}".format(i, self.chi2Values[i][0]))
        print("=" * 80)


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
    # I2.printMatrix()
    I2.chiKwadrat()
    # I2.outPutJSDval()
    I2.printResults()
