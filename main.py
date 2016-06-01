from controler import Controler

file = Controler('textfiles\\text.txt')
file.readFile()
file.splitText()
file.counter()
file.reverseDict()
print('==================================')
print('Time to parse our text document!')
print('==================================')
while True:
    print('Chose option:')
    print('1. Count amount of words in document.')
    print('2. Count each word\'s amount in document.')
    print('0. Exit')
    desizion = input('Enter desizion : ')
    if desizion == '1':
        file.outPutAll()
    if desizion == '2':
        inp = input('Would you like to write into file(press 1) or show here(press 2): ')
        if inp == '1':
            file.writeFile()
            continue
        elif inp == '2':
            file.outPut()
            continue
        else:
            print('Wrong input!' * 3)
    if desizion == '0':
        exit()
    else:
        print()
        print('Wrong desizion! Try again!')
        print()
