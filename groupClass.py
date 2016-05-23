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
            #tmp = Controler.isSpecNumOrSym(self, tmp)
            for j in tmp:
                self.resList.append(j)
            #Controler.cleanList(self, self.resList)
            Group.removeStopWords(self)
        return self.resList

    def removeStopWords(self):
        for x in self.resList:
            if x in self.stopWordsList:
                self.resList.remove(x)
            else:
                continue
        return self.resList

    def groupSentence(self):
        sentenceStart = True
        for x in self.resList:
            if sentenceStart:
                termList = []
                currentSentence = Sentence()
                sentenceStart = False
            if x.endswith('.') or x.endswith('!') or x.endswith('?'):
                x = x[:-1]
                sentenceStart = True
                currentTerm = Term(x, currentSentence)
                termList.append(currentTerm)
                currentSentence.termList = termList
                print()
                print('WORD = {0} | SENTENCE = {1}'.format(currentTerm.word, currentSentence))
                print('Current Term = ', currentTerm)
                #print()
                #print('Term List =', termList)
                print()
                print('CURRENT SENTENCE = ',currentSentence)
                print('CURRENT SENTENCE LIST= ', currentSentence.termList)
                print()
                continue
            currentTerm = Term(x, currentSentence)
            print()
            print('WORD = {0} | SENTENCE = {1}'.format(currentTerm.word, currentSentence))
            print('Current Term = ', currentTerm)
            print()
            termList.append(currentTerm)

if __name__ == '__main__':
    I2 = Group()
    # print(I2.readFromStopWords())
    # print(I2.readFile())
    # print('split text = ',I2.splitText())
    # print('counter = ',I2.counter()) #MAP dict(without stopwords)
    I2.readFromStopWords()
    I2.readFile()
    I2.splitText()
    I2.counter()
    I2.groupSentence()