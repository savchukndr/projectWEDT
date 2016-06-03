import sys

from controller.Groupping import Groupping


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

    print('{0:30.30} {1}'.format('Plik:', filePath))
    print('{0:30.30} {1}'.format('Język:', language))
    print('{0:30.30} {1}'.format('Liczba słów kluczowych:', str(numberOfKeywords)))

    I2 = Groupping(filePath, language)
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
