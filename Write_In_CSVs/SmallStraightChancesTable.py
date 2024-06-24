import csv
import random as rd
import ast

filename = "tableChanceForSS.csv"

diceValues = range(1,7)
numberOfDices = 5

allPossible1DiceKept = [0,1,2,3,4]
allPossible2DiceKept = [(0,1), (0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]
allPossible3DiceKept = [(0,1,2), (0,1,3), (0,1,4), (0,2,3), (0,2,4), (0,3,4), (1,2,3), (1,2,4), (1,3,4), (2,3,4)]
allPossible4DiceKept = [(0,1,2,3), (0,1,2,4), (0,1,3,4), (0,2,3,4), (1,2,3,4)]
listOfDicePositions  = [[] for _ in range(4)] 


def readCSVFile(filename):
    tableChances = {}
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row['Combination']
            one_chance = float(row['OneChance'])
            one_kept_positions = ast.literal_eval(row['OneKeptPositions'])
            tableChances[key] = {
                'OneChance': one_chance,
                'OneKeptPositions': one_kept_positions
            }
    return tableChances 


tableChances = readCSVFile(filename)

def generateRolls(n, k=6):
    if n:
        for i in range(k, 0, -1):
            for roll in generateRolls(n-1, i):
                yield roll + [i]
    else:
        yield []
        
def checkSmallStraight(combination):
    freqVector = [0] * 7
    auxCombination = sorted(combination)
    hitSS = 0
    
    for i in range(len(auxCombination)):
        freqVector[auxCombination[i]] += 1
        
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
    return hitSS

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

def uniqueCombinationDice0(combination, halfFull):
    outcomeZero = list(generateRolls(5))
    totalHits = 0
    totalChances = 0
    chanceToHit = 0
    
    if not halfFull:
        for finalCombination in outcomeZero:
            hitFH = checkSmallStraight(finalCombination)
            if hitFH:
                totalHits += 1
        chanceToHit = totalHits / len(outcomeZero)
    else:
        for finalCombination in outcomeZero:
            provKey = createTableKey(finalCombination)
            totalChances += tableChances[provKey]['OneChance']
        chanceToHit = totalChances / len(outcomeZero)
    return chanceToHit


def uniqueCombinationDice1(combination, halfFull):
    outcomeOne = []
    localMaximumChance = 0
    allPossible1DiceKept = checkForIdenticPairs(combination, 1)
    for pKD in allPossible1DiceKept:
        savedDice = combination[pKD]
        outcomeOne = list(generateRolls(4))
        totalHits = 0
        if not halfFull:
            for finalCombination in outcomeOne:
                finalCombination.append(savedDice)
                hitFH = checkSmallStraight(finalCombination)
                if hitFH:
                    totalHits += 1
            chanceToHit = totalHits / len(outcomeOne)
        else:
            for finalCombination in outcomeOne:
                finalCombination.append(savedDice)
                provKey = createTableKey(finalCombination)
                totalHits += tableChances[provKey]['OneChance']
            chanceToHit = totalHits / len(outcomeOne)
        if chanceToHit > localMaximumChance:
            localMaximumChance = chanceToHit
            listOfDicePositions[0] = list([pKD])
    return localMaximumChance

def uniqueCombinationDice2(combination, halfFull):    
    outcomeTwo = []
    localMaximumChance = 0
    allPossible2DiceKept = checkForIdenticPairs(combination, 2)
    for pKD1, pKD2 in allPossible2DiceKept:
        savedDice = [combination[pKD1], combination[pKD2]]
        outcomeTwo = list(generateRolls(3))
        totalHits = 0
        if not halfFull:
            for finalCombination in outcomeTwo:
                finalCombination.append(savedDice[0])
                finalCombination.append(savedDice[1])
                hitFH = checkSmallStraight(finalCombination)
                if hitFH:
                    totalHits += 1
            chanceToHit = totalHits / len(outcomeTwo)
        else:
            for finalCombination in outcomeTwo:
                finalCombination.append(savedDice[0])
                finalCombination.append(savedDice[1])
                provKey = createTableKey(finalCombination)
                totalHits += tableChances[provKey]['OneChance']
            chanceToHit = totalHits / len(outcomeTwo)
        if chanceToHit > localMaximumChance:
            localMaximumChance = chanceToHit
            listOfDicePositions[1] = list([pKD1, pKD2])
    return localMaximumChance

def uniqueCombinationDice3(combination, halfFull):
    outcomeThree = []
    localMaximumChance = 0
    allPossible3DiceKept = checkForIdenticPairs(combination, 3)
    for pKD1, pKD2, pKD3 in allPossible3DiceKept:
        savedDice = [combination[pKD1], combination[pKD2], combination[pKD3]]
        outcomeThree = list(generateRolls(2))
        totalHits = 0
        if not halfFull:
            for finalCombination in outcomeThree:
                finalCombination.append(savedDice[0])
                finalCombination.append(savedDice[1])
                finalCombination.append(savedDice[2])
                hitFH = checkSmallStraight(finalCombination)
                if hitFH:
                    totalHits += 1
            chanceToHit = totalHits / len(outcomeThree)
        else:
            for finalCombination in outcomeThree:
                finalCombination.append(savedDice[0])
                finalCombination.append(savedDice[1])
                finalCombination.append(savedDice[2])
                provKey = createTableKey(finalCombination)
                totalHits += tableChances[provKey]['OneChance']
            chanceToHit = totalHits / len(outcomeThree)
        if chanceToHit > localMaximumChance:
            localMaximumChance = chanceToHit
            listOfDicePositions[2] = list([pKD1, pKD2, pKD3])
    return localMaximumChance

def uniqueCombinationDice4(combination, halfFull):
    outcomeFour = []
    localMaximumChance = 0
    allPossible4DiceKept = checkForIdenticPairs(combination, 4)
    for pKD1, pKD2, pKD3, pKD4 in allPossible4DiceKept:
        partialCombination = [combination[pKD1], combination[pKD2], combination[pKD3], combination[pKD4], 0]
        outcomeFour = list(generateRolls(1))
        totalHits = 0
        if not halfFull:
            for finalDice in outcomeFour:
                partialCombination[4] = finalDice[0]
                hitFH = checkSmallStraight(partialCombination)
                if hitFH:
                    totalHits += 1
            chanceToHit = totalHits / len(outcomeFour)
        else:
            for finalDice in outcomeFour:
                partialCombination[4] = finalDice[0]
                provKey = createTableKey(partialCombination)
                totalHits += tableChances[provKey]['OneChance']
            chanceToHit = totalHits / len(outcomeFour)
        if chanceToHit > localMaximumChance:
            localMaximumChance = chanceToHit
            listOfDicePositions[3] = list([pKD1, pKD2, pKD3, pKD4])
    return localMaximumChance

def expectiMaxForTable(combination, halfFull):
    defaultChance = checkSmallStraight(combination)
    expectiMaxChances = [0] * 6
    if defaultChance:
        expectiMaxChances[-1] = 1
    for noOfDicesKept in range(5):
        if noOfDicesKept == 0:
            expectiMaxChances[noOfDicesKept] = uniqueCombinationDice0(combination, halfFull)
        elif noOfDicesKept == 1:
            expectiMaxChances[noOfDicesKept] = uniqueCombinationDice1(combination, halfFull)
        elif noOfDicesKept == 2:
            expectiMaxChances[noOfDicesKept] = uniqueCombinationDice2(combination, halfFull)
        elif noOfDicesKept == 3:
            expectiMaxChances[noOfDicesKept] = uniqueCombinationDice3(combination, halfFull)
        elif noOfDicesKept == 4:
            expectiMaxChances[noOfDicesKept] = uniqueCombinationDice4(combination, halfFull)
    for dice, chance in enumerate(expectiMaxChances):
        if chance >= defaultChance:
            defaultChance = chance
            numberOfDices = dice
    keptPositions = []
    if numberOfDices == 5:
        keptPositions = [0,1,2,3,4]
    elif numberOfDices == 0:
        keptPositions = []
    else:
        keptPositions = listOfDicePositions[numberOfDices - 1]
    return defaultChance, keptPositions

def CreateExpectiMaxTable():
    expectiMaxAllOutcomesTable = {}
    allPossibleCombinations = list(generateRolls(5))
    for combination in allPossibleCombinations:
        key = createTableKey(combination)
        oneActionChance, oneActionPositions = expectiMaxForTable(combination, 0)
        twoActionChance, twoActionPositions = expectiMaxForTable(combination, 1)
        expectiMaxAllOutcomesTable[key] = (twoActionChance, twoActionPositions, oneActionChance, oneActionPositions)
    return expectiMaxAllOutcomesTable

def writeCSVFile():
    table = CreateExpectiMaxTable()
    fields = ['Combination', 'TwoChance', 'TwoKeptPositions', 'OneChance', 'OneKeptPositions']
    #filename = "tableChanceForSS.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        rows = [{'Combination': key, 'TwoChance': value[0], 'TwoKeptPositions': value[1], 'OneChance': value[2], 'OneKeptPositions': value[3]} for key, value in table.items()]
        writer.writerows(rows)

writeCSVFile()

