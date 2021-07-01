import random
def int_to_list(n):
    n=str(n)
    l=list(n)
    return l

class CowsAndBulls:
    def __init__(self):
        self.number = ""
        self.digits = 0
        self.active = False

    def makeRandom(self, digit):
        digits = set(range(10))
        first = random.randint(1, 9)
        second_to_last = random.sample(digits - {first}, digit-1)
        botNumber = str(first) + ''.join(map(str, second_to_last))
        return botNumber

    def compareNumbers(numA, numB):
        if(len(numA)!=len(numB)):
            return -1, -1
        
        else:
            bulls=0
            cows=0
            n1 = int(numA)
            n2 = int(numB)
            l1 = int_to_list(n1)
            l2 = int_to_list(n2)
            i = 0
            for digit in l1:
                if digit == l2[i]:
                    bulls+=1
                    l2[i]='a'
                i+=1
            
            for digit in l1:
                for dig in l2:
                    if dig==digit:
                        cows+=1
            
            return bulls, cows
