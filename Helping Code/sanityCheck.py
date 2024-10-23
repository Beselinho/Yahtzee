import random as rd

def checkFullHouse(combination):
    freqVector = [0] * 7
    for die in combination:
        freqVector[die] += 1
    sortedFreq = sorted(freqVector)
    return sortedFreq[-1] == 3 and sortedFreq[-2] == 2

def checkSmallStraight(combination):
    freqVector = [0] * 7
    
    for die in combination:
        freqVector[die] += 1

    # Check for consecutive sets
    for start in range(1, 4):  # Only three possible starts (1, 2, 3)
        if all(freqVector[start + i] > 0 for i in range(4)):
            return True

    return False

def checkFourOfAKind(combination):
    freqVector = [0] * 6
    for die in combination:
        freqVector[die - 1] += 1
    for no in freqVector:
        if no >= 4:
            return True
    return False


def rollDice(num_dice):
    return [rd.randint(1, 6) for _ in range(num_dice)]

def sanityCheck(numSimulations):
    hitsFH = 0
    hitsSS = 0
    hitsFoaK = 0
    for _ in range(numSimulations):
        combination = rollDice(4)
        combination.append(1)
        if checkFullHouse(combination):
            hitsFH += 1
        if checkSmallStraight(combination):
            hitsSS += 1
        if checkFourOfAKind(combination):
            hitsFoaK += 1
    
    return hitsFH / numSimulations #hitsFH / numSimulations, hitsSS / numSimulations, (hitsFH + hitsSS) / numSimulations

numSimulations = 1000000  # 1 million
#noFH, noSS, total = sanityCheck(numSimulations)

noFH = sanityCheck(numSimulations)
print("Chances of Full Houses: ", noFH * 100, "%")
# print("Chances of Small Straights: ", noSS * 100, "%")
# print("Total chances of hits: ", total * 100, "%")

# noFoaK = sanityCheck(numSimulations)
# print("Chances of Four of a Kind: ", noFoaK * 100, "%")

#FullHouse = 3.85%
#SmallStraight = 15.3%
#Total = 19.2%

