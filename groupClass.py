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
                #if x == 'termword':
                #    self.resListSplitWithDots.remove(x)
                x = x[:-1]
                sentenceStart = True
                currentTerm = Term(x, currentSentence)
                self.termList.append(currentTerm)
                #currentSentence.termList = termList
                #sent.sentenceList.append(currentSentence)
                #self.sentenceList1.append(currentSentence)
                #self.currentSentence = currentSentence.termList
                self.sentenceList.append(currentSentence)
                print()
                print('WORD = {0} | SENTENCE = {1}'.format(currentTerm.word, currentSentence))
                print('Current Term = ', currentTerm)
                #print('CURRENT SENTENCE = ',currentSentence)
                print()
                continue
            currentTerm = Term(x, currentSentence)
            self.termList.append(currentTerm)
            print()
            print('WORD = {0} | SENTENCE = {1}'.format(currentTerm.word, currentSentence))
            print('Current Term = ', currentTerm)
            print()
            #termList.append(currentTerm)

    def remove30percent(self):
        indexToCut = round(len(self.ret) * 0.3)
        self.ret30percent = self.ret[:indexToCut]
        self.ret30percentG = {}
        for (x, y) in self.ret30percent:
            self.ret30percentG[x] = y
        print('GDict =', self.ret30percentG)
        return self.ret30percent

    def matrixOfApearanceWords(self):
        #print(self.sentenceList)
        self.D = {}
        self.tmp = {}
        print('sentence LIST =', self.sentenceList)
        print('term LIST =', self.termList)
        #for (i, j) in self.ret:
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
        '''
            for x in self.currentSentense:
                print('word =', x.word)
                print('sentence =', x.sentence)
            for (x, y) in self.ret30percent:
                if x in self.currentSentense:
                    print('ok')
                else:
                    print('ne ok')
            '''

if __name__ == '__main__':
    I2 = Group()
    I2.readFromStopWords()
    I2.readFile()
    print()
    print('resList = ', I2.splitText())
    print('MAP = ', I2.counter()) #MAP dict(without stopwords)
    print('Reversed MAP =', I2.reverseDict())
    print()

    print('G = ',I2.remove30percent())

    #I2.readFromStopWords()
    #I2.readFile()
    #I2.splitText()
    #I2.counter()
    I2.groupSentence()
    I2.matrixOfApearanceWords()