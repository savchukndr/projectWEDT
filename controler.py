from collections import OrderedDict

class Controler:
    def __init__(self, file):
        self.file = file

    # read from file
    def readFile(self):
        f = open(self.file)
        self.string = f.read()
        f.close()
        return self.string

    #write into file
    def writeFile(self):
        f = open('results.txt', 'w')
        for (key, value) in self.ret:
            f.write('\"{0}\" is {1} times\n'.format(key, value))
        print()
        print('ADDED!')
        print()
        f.close()

    # function for cleaning list from ''
    def cleanList(self, lst):
        for x in lst:
            if x == '':
                lst.remove(x)
        return lst

    # reduse all special symbols and digis
    def isSpecNumOrSym(self, lst):
        tmp = []
        s = ''
        for x in lst:
            for z in range(len(x)):
                if x[0] in ['/', '\\', '(', ')']:
                    x = x[1:]
                else:
                    break
            if ('/' in x) or ('\\' in x) or ('(' in x) or (')' in x):
                for z in range(len(x)):
                    if x[z] not in ['/', '\\', '(', ')']:
                        s += x[z]
                        continue
                    else:
                        if s == '':
                            continue
                        else:
                            tmp.append(s)
                            s = ''
            else:
                tmp.append(x)
        tmp.append(s)
        lst = tmp
        res = []
        for x in lst:
            x = x.lower()
            s = ''.join(e for e in x if e.isalnum())
            s = ''.join(e for e in s if e not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
            res.append(s)
            Controler.cleanList(self, res)
        #print(res)
        return res

    # splting text frome file into single words in list
    def splitText(self):
        self.listNsplit = self.string.split('\n')
        self.resList = []
        for i in self.listNsplit:
            tmp = i.split(' ')
            tmp = Controler.isSpecNumOrSym(self, tmp)
            for j in tmp:
                self.resList.append(j)
            Controler.cleanList(self, self.resList)
        return self.resList

    # counting amount of words in text
    def counter(self):
        self.D = {}
        for x in self.resList:
            count = self.resList.count(x)
            self.D[x] = count
        return self.D

    # reverse dictionary from up to down
    def reverseDict(self):
        ret = OrderedDict(sorted(self.D.items(), key=lambda x: x[0], reverse=False))
        self.ret = sorted(ret.items(), key=lambda x: x[1], reverse=True)
        #print(self.ret)
        return self.ret

    # printing results
    def outPut(self):
        for (key, value) in self.ret:
            print('---------------------------------------------')
            print('\"{0}\" is {1} times'.format(key, value))
        print('---------------------------------------------')
        print()

    # print word's amount in document
    def outPutAll(self):
        print('=============================================')
        print('Whole word\'s amount is {0}'.format(len(self.ret)))
        print('=============================================')
        print()


if __name__ == '__main__':
    I1 = Controler('text.txt')
    I1.readFile()
    I1.splitText()
    I1.counter()
    I1.reverseDict()
    I1.outPut()



