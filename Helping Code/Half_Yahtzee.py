diceValues = range(1,7)
numberOfDices = 5
allPossible2DiceKept = [(0,1), (0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]
allPossible3DiceKept = [(0,1,2), (0,1,3), (0,1,4), (0,2,3), (0,2,4), (0,3,4), (1,2,3), (1,2,4), (1,3,4), (2,3,4)]
allPossible4DiceKept = [(0,1,2,3), (0,1,2,4), (0,1,3,4), (0,2,3,4), (1,2,3,4)]
listOfDicePositions = [[] for _ in range(4)] 



def checkSmallStraight(combination):
    freqVector = [0] * 7
    
    for die in combination:
        freqVector[die] += 1

    # Check for consecutive sets
    for start in range(1, 4):  # Only three possible starts (1, 2, 3)
        if all(freqVector[start + i] > 0 for i in range(4)):
            return True

    return False

def checkFullHouse(combination):
    freqVector = [0] * 7
    for die in combination:
        freqVector[die] += 1
    sortedFreq = sorted(freqVector)
    return sortedFreq[-1] == 3 and sortedFreq[-2] == 2


def generateRolls(n, k=6):
    if n:
        for i in range(k, 0, -1):
            for roll in generateRolls(n-1, i):
                yield roll + [i]
    else:
        yield []

nr = 0
allC = list(generateRolls(5))
for c in allC:
    if checkFullHouse(c):
        print(c, "\n")
        nr += 1

print("-------------", nr)
        
def checkScore(combination):
    auxCombination = sorted(combination)
    freqVector = [0] * 7
    score = 0
    localScore = 0
    fullHousePoints = 25
    smallStraightPoints = 30
    largeStraightPoints = 40
    YahtzeePoints = 50
    hitSS = 0
    
    for i in range(len(auxCombination)):
        freqVector[auxCombination[i]] += 1
        
    #Hit Vector
    # 0    1    2     3    4     5    6
    # TK   FK   FH    SS   LS    CH   Y        
    #hitVector = [0] * 7
    #print(freqVector)
    
    #Upper-Side
    for i in range(1,len(freqVector)):
        localScore = i * freqVector[i]
        if localScore > score:
            score = localScore
        
    #Three-of-a-kind
    for no in freqVector:
        if no == 3:
            localScore = sum(auxCombination)
            if(localScore > score):
                #hitVector[0] = 1
                score = localScore
                
    #Four-of-a-kind
    for no in freqVector:
        if no == 4:
            localScore = sum(auxCombination)
            if(localScore > score):
                #hitVector[1] = 1
                score = localScore
                
    #Full-House
    sortedFreq = sorted(freqVector)
    if sortedFreq[-1] == 3 and sortedFreq[-2] == 2:
        score = fullHousePoints
        if(fullHousePoints > score):
            score = fullHousePoints
      
    #Small-Straight
    count = 0
    for app in freqVector[1:5]:
        if app >= 1:
            count += 1
        if count == 4:
            hitSS = 1
            break
    count = 0
    for app in freqVector[2:6]:
        if app >= 1:
            count += 1
        if count == 4:
            hitSS = 1
            break
    count = 0
    for app in freqVector[3:7]:
        if app >= 1:
            count += 1
        if count == 4:
            hitSS = 1
            break
    if hitSS == 1:
        localScore = smallStraightPoints
        if localScore > score:
            score = localScore
            
    #Large-Straight
    largeSequence1 = [1,2,3,4,5]
    largeSequence2 = [2,3,4,5,6]
    if auxCombination == largeSequence1 or auxCombination == largeSequence2:
        score = largeStraightPoints
        if(largeStraightPoints > score):
            score = largeStraightPoints
    
    #Yahtzee
    for no in freqVector:
        if no == 5:
            score = YahtzeePoints
            
    #Chance
        localScore = sum(auxCombination)
        if(localScore > score):
            score = localScore
            
    return score

def uniqueCombinationDice0(combination):
    outcomeZero = []
    localMaximum = 0
    outcomeZero = list(generateRolls(5))
    totalScore = 0
    for finalCombination in outcomeZero:
        score = checkScore(finalCombination)
        totalScore += score
    
    totalScore = totalScore / len(outcomeZero)
    if totalScore > localMaximum:
        localMaximum = totalScore
    
    return localMaximum

def uniqueCombinationDice1(combination):
    outcomeOne = []
    localMaximum = 0
    for pKD in range(5):
        savedDice = combination[pKD]
        outcomeOne = list(generateRolls(4))
        totalScore = 0
        for finalCombination in outcomeOne:
            finalCombination.append(savedDice)
            score = checkScore(finalCombination)
            totalScore += score
            
        totalScore = totalScore / len(outcomeOne)
        if totalScore > localMaximum:
            localMaximum = totalScore
            listOfDicePositions[0] = list([pKD])
        
    return localMaximum

def uniqueCombinationDice2(combination):
    outcomeTwo = []
    localMaximum = 0
    for pKD1, pKD2 in allPossible2DiceKept:
        savedDice = [combination[pKD1], combination[pKD2]]
        outcomeTwo = list(generateRolls(3))
        totalScore = 0
        for finalCombination in outcomeTwo:
            finalCombination.append(savedDice[0])
            finalCombination.append(savedDice[1])
            score = checkScore(finalCombination)
            totalScore += score
        
        totalScore = totalScore / len(outcomeTwo)
        if totalScore > localMaximum:
            localMaximum = totalScore
            listOfDicePositions[1] = list([pKD1, pKD2])
    
    return localMaximum

def uniqueCombinationDice3(combination):
    outcomeThree = []
    localMaximum = 0
    for pKD1, pKD2, pKD3 in allPossible3DiceKept:
        savedDice = [combination[pKD1], combination[pKD2], combination[pKD3]]
        outcomeThree = list(generateRolls(2))
        totalScore = 0
        for finalCombination in outcomeThree:
            finalCombination.append(savedDice[0])
            finalCombination.append(savedDice[1])
            finalCombination.append(savedDice[2])
            score = checkScore(finalCombination)
            totalScore += score
            # print("combination :", finalCombination, "with score :", score)
            
        
        totalScore = totalScore / len(outcomeThree)
        if totalScore > localMaximum:
            localMaximum = totalScore
            listOfDicePositions[2] = list([pKD1, pKD2, pKD3])
    
    return localMaximum

def uniqueCombinationDice4(combination):
    outcomeFour = []
    localMaximum = 0
    #pKD = positionKeptDice
    for pKD1, pKD2, pKD3, pKD4 in allPossible4DiceKept:
        partialCombination = [combination[pKD1], combination[pKD2], combination[pKD3], combination[pKD4], 0]
        outcomeFour = list(generateRolls(1))
        totalScore = 0
        for finalDice in outcomeFour:
            partialCombination[4] = finalDice[0]
            score = checkScore(partialCombination)
            totalScore += score
        
        totalScore = totalScore / len(outcomeFour)
        if totalScore > localMaximum:
            localMaximum = totalScore
            #print(pKD1, pKD2, pKD3, pKD4)
            listOfDicePositions[3] = list([pKD1, pKD2, pKD3, pKD4])
              
    return localMaximum        
        
    
def expectiMax(combination):
    defaultScore = checkScore(combination)
    numberOfDices = 0
    expectiMaxScore = [0] * 6
    expectiMaxScore[-1] = defaultScore
    for noOfDicesKept in range(5):
        if noOfDicesKept == 0:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice0(combination)
        elif noOfDicesKept == 1:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice1(combination)
        elif noOfDicesKept == 2:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice2(combination)
        elif noOfDicesKept == 3:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice3(combination)
        elif noOfDicesKept == 4:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice4(combination)
                  
    print("ExpectiMax scores for each number of dice kept:\n")
    for i in range(len(expectiMaxScore)):
        print("Number of dices kept :", i, "with score :", expectiMaxScore[i])
    
    for dice, score in enumerate(expectiMaxScore):
        if score >= defaultScore:
            defaultScore = score
            numberOfDices = dice
            
    print("\nExpecti Max Score chosen :", defaultScore, "\n")
    
    if numberOfDices == 0:
        print("All dices were rolled")
    elif numberOfDices == 5:
        print("All dices were kept")
    else:
        print("Number of dice kept :", numberOfDices)
        print("Positions of the kept dices :", listOfDicePositions[numberOfDices - 1])
    
            
    


def expectiMaxForTable(combination):
    defaultScore = checkScore(combination)
    expectiMaxScore = [0] * 6
    expectiMaxScore[-1] = defaultScore
    for noOfDicesKept in range(5):
        if noOfDicesKept == 0:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice0(combination)
        elif noOfDicesKept == 1:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice1(combination)
        elif noOfDicesKept == 2:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice2(combination)
        elif noOfDicesKept == 3:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice3(combination)
        elif noOfDicesKept == 4:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice4(combination)
    
    for score in expectiMaxScore:
        if score >= defaultScore:
            defaultScore = score
    
    return defaultScore

def createTableKey(combination):
    freqVector = [0] * 6
    for diceFace in combination:
      freqVector[diceFace - 1] += 1
    
    key = ''.join(str(freqVector[i]) for i in range(len(freqVector)))
    return key  
    
def expectiMaxTable():
    expectiMaxAllOutcomesTable = {}
    allPossibleCombinations = list(generateRolls(5))
    for combination in allPossibleCombinations:
        key = createTableKey(combination)
        expectiMaxAllOutcomesTable[key] = expectiMaxForTable(combination) 
    
    return  expectiMaxAllOutcomesTable


#Table = expectiMaxTable()
#print(expectiMax([2,3,4,4,5]))
#print(expectiMax([5,4,1,3,3]))

    
        
        


            


