import csv

diceValues = range(1,7)
numberOfDices = 5

allPossible1DiceKept = [0,1,2,3,4]
allPossible2DiceKept = [(0,1), (0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]
allPossible3DiceKept = [(0,1,2), (0,1,3), (0,1,4), (0,2,3), (0,2,4), (0,3,4), (1,2,3), (1,2,4), (1,3,4), (2,3,4)]
allPossible4DiceKept = [(0,1,2,3), (0,1,2,4), (0,1,3,4), (0,2,3,4), (1,2,3,4)]
listOfDicePositions  = [[] for _ in range(4)] 

combinationName = {
   0 : "Three of a Kind",
   1: "Four of a Kind",
   2: "Full House",
   3: "Small Straight",
   4: "Large Straight",
   5: "Yahtzee",
   6: "Chance"
}


def generateRolls(n, k=6):
    if n:
        for i in range(k, 0, -1):
            for roll in generateRolls(n-1, i):
                yield roll + [i]
    else:
        yield []

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
    combHit = -1
    
    for i in range(len(auxCombination)):
        freqVector[auxCombination[i]] += 1
        
    
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
                combHit = 0
                score = localScore
                
    #Four-of-a-kind
    for no in freqVector:
        if no == 4:
            localScore = sum(auxCombination)
            if(localScore > score):
                combHit = 1
                score = localScore
                
    #Full-House
    sortedFreq = sorted(freqVector)
    if sortedFreq[-1] == 3 and sortedFreq[-2] == 2:
        score = fullHousePoints
        if(fullHousePoints > score):
            combHit = 2
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
            combHit = 3
            score = localScore
            
    #Large-Straight
    largeSequence1 = [1,2,3,4,5]
    largeSequence2 = [2,3,4,5,6]
    if auxCombination == largeSequence1 or auxCombination == largeSequence2:
        score = largeStraightPoints
        if(largeStraightPoints > score):
            combHit = 4
            score = largeStraightPoints
    
    #Yahtzee
    for no in freqVector:
        if no == 5:
            combHit = 5
            score = YahtzeePoints
            
    #Chance
        localScore = sum(auxCombination)
        if(localScore > score):
            combHit = 6
            score = localScore
            
    return score, combHit

def createTableKey(combination):
    freqVector = [0] * 6
    for diceFace in combination:
      freqVector[diceFace - 1] += 1
    
    key = ''.join(str(freqVector[i]) for i in range(len(freqVector)))
    return key  

def checkForIdenticPairs(combination, diceNumber):
    appearanceVector = [0] * 7
    appearanceCounter = [[] for _ in range(10)]
    filteredPositions = []

    if diceNumber == 1:
        for pos in allPossible1DiceKept:
            if not appearanceVector[combination[pos]]:
                appearanceVector[combination[pos]] = True
                filteredPositions.append(pos)
                
        return filteredPositions

    elif diceNumber == 2:
        for pos in allPossible2DiceKept:
            faceValues = [combination[pos[0]], combination[pos[1]]]
            if faceValues not in appearanceCounter:
                appearanceCounter.append(faceValues)
                filteredPositions.append(pos)
                
        return filteredPositions

    elif diceNumber == 3:
        for pos in allPossible3DiceKept:
            faceValues = [combination[pos[0]], combination[pos[1]], combination[pos[2]]]
            if faceValues not in appearanceCounter:
                appearanceCounter.append(faceValues)
                filteredPositions.append(pos)
                
        return filteredPositions

    elif diceNumber == 4:
        for pos in allPossible4DiceKept:
            faceValues = [combination[pos[0]], combination[pos[1]], combination[pos[2]], combination[pos[3]]]
            if faceValues not in appearanceCounter:
                appearanceCounter.append(faceValues)
                filteredPositions.append(pos)
                
        return filteredPositions

def halfUniqueCombinationDice0(combination):
    outcomeZero = []
    localMaximum = 0
    outcomeZero = list(generateRolls(5))
    totalScore = 0
    for finalCombination in outcomeZero:
        score, _ = checkScore(finalCombination)
        totalScore += score
    
    totalScore = totalScore / len(outcomeZero)
    if totalScore > localMaximum:
        localMaximum = totalScore
    
    return localMaximum

def halfUniqueCombinationDice1(combination):
    outcomeOne = []
    localMaximum = 0
    #allPossible1DiceKept = checkForIdenticPairs(combination, 1)
    for pKD in allPossible1DiceKept:
        savedDice = combination[pKD]
        outcomeOne = list(generateRolls(4))
        totalScore = 0
        for finalCombination in outcomeOne:
            finalCombination.append(savedDice)
            score, _ = checkScore(finalCombination)
            totalScore += score
            
        totalScore = totalScore / len(outcomeOne)
        if totalScore > localMaximum:
            localMaximum = totalScore
            listOfDicePositions[0] = list([pKD])
        
    return localMaximum

def halfUniqueCombinationDice2(combination):
    outcomeTwo = []
    localMaximum = 0
    #allPossible2DiceKept = checkForIdenticPairs(combination, 2)
    for pKD1, pKD2 in allPossible2DiceKept:
        savedDice = [combination[pKD1], combination[pKD2]]
        outcomeTwo = list(generateRolls(3))
        totalScore = 0
        for finalCombination in outcomeTwo:
            finalCombination.append(savedDice[0])
            finalCombination.append(savedDice[1])
            score, _ = checkScore(finalCombination)
            totalScore += score
        
        totalScore = totalScore / len(outcomeTwo)
        if totalScore > localMaximum:
            localMaximum = totalScore
            listOfDicePositions[1] = list([pKD1, pKD2])
    
    return localMaximum

def halfUniqueCombinationDice3(combination):
    outcomeThree = []
    localMaximum = 0
    #allPossible3DiceKept = checkForIdenticPairs(combination, 3)
    for pKD1, pKD2, pKD3 in allPossible3DiceKept:
        savedDice = [combination[pKD1], combination[pKD2], combination[pKD3]]
        outcomeThree = list(generateRolls(2))
        totalScore = 0
        for finalCombination in outcomeThree:
            finalCombination.append(savedDice[0])
            finalCombination.append(savedDice[1])
            finalCombination.append(savedDice[2])
            score, _ = checkScore(finalCombination)
            totalScore += score
        
        totalScore = totalScore / len(outcomeThree)
        if totalScore > localMaximum:
            localMaximum = totalScore
            listOfDicePositions[2] = list([pKD1, pKD2, pKD3])
            
        
        return localMaximum

def halfUniqueCombinationDice4(combination):
    outcomeFour = []
    localMaximum = 0
    #pKD = positionKeptDice
    #allPossible4DiceKept = checkForIdenticPairs(combination, 4)
    for pKD1, pKD2, pKD3, pKD4 in allPossible4DiceKept:
        partialCombination = [combination[pKD1], combination[pKD2], combination[pKD3], combination[pKD4], 0]
        outcomeFour = list(generateRolls(1))
        totalScore = 0
        for finalDice in outcomeFour:
            partialCombination[4] = finalDice[0]
            score, _ = checkScore(partialCombination)
            totalScore += score
        
        totalScore = totalScore / len(outcomeFour)
        if totalScore > localMaximum:
            localMaximum = totalScore
            #print(pKD1, pKD2, pKD3, pKD4)
            listOfDicePositions[3] = list([pKD1, pKD2, pKD3, pKD4])
              
    return localMaximum

def expectiMaxForTable(combination):
    defaultScore, combHit = checkScore(combination)
    expectiMaxScore = [0] * 6
    expectiMaxScore[-1] = defaultScore
    for noOfDicesKept in range(5):
        if noOfDicesKept == 0:
            expectiMaxScore[noOfDicesKept] = halfUniqueCombinationDice0(combination)
        elif noOfDicesKept == 1:
            expectiMaxScore[noOfDicesKept] = halfUniqueCombinationDice1(combination)
        elif noOfDicesKept == 2:
            expectiMaxScore[noOfDicesKept] = halfUniqueCombinationDice2(combination)
        elif noOfDicesKept == 3:
            expectiMaxScore[noOfDicesKept] = halfUniqueCombinationDice3(combination)
        elif noOfDicesKept == 4:
            expectiMaxScore[noOfDicesKept] = halfUniqueCombinationDice4(combination)
    
    for score in expectiMaxScore:
        if score >= defaultScore:
            defaultScore = score
    
    return defaultScore, combHit
    
def CreateExpectiMaxTable():
    expectiMaxAllOutcomesTable = {}
    allPossibleCombinations = list(generateRolls(5))
    for combination in allPossibleCombinations:
        key = createTableKey(combination)
        expectiMaxAllOutcomesTable[key] = expectiMaxForTable(combination) 
    
    return  expectiMaxAllOutcomesTable


def writeCSVFile():
    table = CreateExpectiMaxTable()
    # for key, value in table.items():
    #     print(key, value)
    fields = ['Combination', 'Score', 'Hit']
    filename = "tableExpectiMax.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        rows = [{'Combination': key, 'Score': value[0], 'Hit': value[1]} for key, value in table.items()]
        writer.writerows(rows)

writeCSVFile()




# ChooseCombination = [2,3,5,5,5]


# allPossible1DiceKept = checkForIdenticPairs(ChooseCombination, 1)
# print("-------------11111111----------", allPossible1DiceKept)
# allPossible2DiceKept = checkForIdenticPairs(ChooseCombination, 2)
# print("-------------22222222----------", allPossible2DiceKept)
# allPossible3DiceKept = checkForIdenticPairs(ChooseCombination, 3)
# print("-------------33333333----------", allPossible3DiceKept)
# allPossible4DiceKept = checkForIdenticPairs(ChooseCombination, 4)
# print("-------------44444444----------", allPossible4DiceKept) 


