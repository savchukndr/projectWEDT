import subprocess
from encodings import utf_8

import sys
from nltk.stem.porter import PorterStemmer
from numpy.linalg import norm
from scipy.stats import entropy

from controler import Controler
from domain.Sentence import Sentence
from domain.Term import Term


class Group(Controler):
    """Class Group"""

    def __init__(self, file, lang='pl'):
        Controler.__init__(self, file=file)
        self.language = lang
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
        if language == 'pl':
            self.morfeuszProcess = subprocess.Popen(['morfeusz_bin\morfeusz_analyzer.exe', '-c', 'UTF8'],
                                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                    bufsize=1)
        else:
            self.porterStemmer = PorterStemmer()  # stemmer for english

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
                if x_stemmed in self.stopWordsList:
                    continue
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

    def stemAWord(self, x: str) -> str:
        if self.language == 'pl':
            return self.stemWithMorfeusz(x)
        else:
            return self.porterStemmer.stem(x)

    def stemWithMorfeusz(self, inputWord: str) -> str:
        self.writeLineToMorfeusz(inputWord)
        line = self.readLineFromMorfeusz()
        morfeuszInputAssumption = self.getMorfeuszInputAssumption(line)

        # hack np. na wyraz "gdybym", "czym", który dostaje 2 outputy
        if morfeuszInputAssumption != inputWord:
            # na wszelki wypadek (np. wyraz "al-islam")
            self.skipResultsWithinSameSection(line)
            # odczytanie "następnego" wyniku, ale tak na prawdę, to bieżącego, bo te złe assumption było z poprzedniego
            line = self.readLineFromMorfeusz()
            # sprawdzamy po raz drugi i ostatni czy assumption jest ok
            morfeuszInputAssumption = self.getMorfeuszInputAssumption(line)
            if morfeuszInputAssumption != inputWord:
                # jeśli nadal nie, to trudno, nie stemujemy (np. wyraz "gdybym")
                return inputWord

        stemmed = self.getMorfeuszStemmedWord(line)
        # print("STEM {0:10.10s} -> {1:10.10s}".format(inputWord, stemmed))
        return stemmed

    def writeLineToMorfeusz(self, x):
        self.morfeuszProcess.stdin.write(utf_8.encode(x + "\n")[0])
        self.morfeuszProcess.stdin.flush()

    def readLineFromMorfeusz(self):
        readBytes = self.morfeuszProcess.stdout.readline()
        line = utf_8.decode(readBytes, errors='replace')[0]
        return line

    def skipResultsWithinSameSection(self, line):
        while not (line.endswith(']\r') or line.endswith(']\n') or line.endswith(']\r\n') or line.endswith(']\n\r')):
            line = self.readLineFromMorfeusz()

    def getMorfeuszStemmedWord(self, line):
        stemmed = line.split(',')[3].split(':')[0]  # bierzemy tylko pierwszy wynik
        self.skipResultsWithinSameSection(line)
        return stemmed

    @staticmethod
    def getMorfeuszInputAssumption(line):
        morfeuszInputAssumption = line.split(',')[2].split(':')[0]
        return morfeuszInputAssumption

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
        # print(self.termSentencesTotalSize)

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
        self.chi2Values.sort(key=lambda x: x[1], reverse=True)
        # print(self.chi2Values)

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

    def printResults(self, keywordsCount: int):
        print("=" * 80)
        print("{0:>3.3s}  {1:20.20s} {2:>12.12s} {3:>10.10s}".format(
            'Lp',
            'Słowo kluczowe',
            'Wystąpienia',
            'chi^2'
        ))
        print("=" * 80)
        for i in range(keywordsCount):
            print("{0:3d}. {1:20.20s} {2:12d} {3:10.2f}".format(
                i + 1,
                self.chi2Values[i][0],
                self.Dict[self.chi2Values[i][0]],
                self.chi2Values[i][1]
            ))
        print("=" * 80)


def printUsage():
    print()
    print('Użycie:')
    print('    program -f=filepath [-l={pl|en}] [-n=numberOfKeywords]')
    exit(-1)


if __name__ == '__main__':
    language = 'pl'
    numberOfKeywords = 20
    filePath = None

    for arg in sys.argv[1:]:
        arg = arg.split('=')
        command = arg[0]
        value = arg[1]
        if command == '-l':
            if value in ['pl', 'en']:
                language = value
            else:
                print('Nieobsługiwana stała języka {0}'.format(value))
                printUsage()
        elif command == '-n':
            if str(value).isdecimal():
                numberOfKeywords = int(value)
            else:
                print('number of keywords musi być liczbą, a jest: {0}'.format(value))
                printUsage()
        elif command == '-f':
            filePath = value
        else:
            print('Nieobsługiwany parametr wejściowy {0}'.format(command))
            printUsage()
    if filePath is None:
        print('Nie podano pliku wejściowego')
        printUsage()

    I2 = Group(filePath, language)
    I2.readFromStopWords()
    I2.readFile()
    I2.splitText()
    I2.counter()
    I2.reverseDict()
    # print('Sorted D =', I2.ret)
    I2.remove30percent()
    # print('Sorted G = ', I2.ret30percent)
    I2.groupSentence()
    I2.matrixOfApearanceWords()
    # I2.printMatrix()
    I2.chiKwadrat()
    # I2.outPutJSDval()
    I2.printResults(numberOfKeywords)
