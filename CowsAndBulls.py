import random

def makeRandom():
    digits = set(range(10))
    first = random.randint(1, 9)
    last_3 = random.sample(digits - {first}, 3)
    botNumber = str(first) + ''.join(map(str, last_3))
    return botNumber

def compareNumbers(numA, numB):
    if(len(numA)!=len(numB)):
        # handle this
        return
    
    else:
        notEqualDigits = []
        i = 0
        cows = 0
        bulls = 0
        for i in range(len(numA)):
            if(numA[i]!=numB[i]):
                notEqualDigits.append(numA[i])
                notEqualDigits.append(numB[i])
            else:
                bulls+=1
        
        for i in range(len(notEqualDigits)):
            for j in range(i+1 , len(notEqualDigits)):
                if(notEqualDigits[i]==notEqualDigits[j]):
                    cows+=1

        return bulls, cows
