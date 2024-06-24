import csv
import random as rd

filename = "tableExpectiMax.csv"

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


def readCSVFile(filename):
    tableValues = {}
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row['Combination']
            score = float(row['Score'])
            hit = row['Hit']
            tableValues[key] = (score, hit)
    
    return tableValues

tableValues = readCSVFile(filename)
# for key, value in tableValues.items():
#     print("combination : ", key, "with expecti score:", value[0], "hitthing : ", value[1])

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



def uniqueCombinationDice0(combination, halfFull):
    outcomeZero = []
    localMaximum = 0
    outcomeZero = list(generateRolls(5))
    totalScore = 0
    for finalCombination in outcomeZero:
        if halfFull == 1:
            provKey = createTableKey(finalCombination)
            totalScore += tableValues[provKey][0]
        else: 
            score, _ = checkScore(finalCombination)
            totalScore += score
    
    totalScore = totalScore / len(outcomeZero)
    if totalScore > localMaximum:
        localMaximum = totalScore
    
    return localMaximum

def uniqueCombinationDice1(combination, halfFull):
    outcomeOne = []
    localMaximum = 0
    allPossible1DiceKept = checkForIdenticPairs(combination, 1)
    for pKD in allPossible1DiceKept:
        savedDice = combination[pKD]
        outcomeOne = list(generateRolls(4))
        totalScore = 0
        for finalCombination in outcomeOne:
            finalCombination.append(savedDice)
            if halfFull == 1:
                provKey = createTableKey(finalCombination)
                totalScore += tableValues[provKey][0]
            else:
                score, _ = checkScore(finalCombination)
                totalScore += score
            
        totalScore = totalScore / len(outcomeOne)
        if totalScore > localMaximum:
            localMaximum = totalScore
            listOfDicePositions[0] = list([pKD])
        
    return localMaximum

def uniqueCombinationDice2(combination, halfFull):
    outcomeTwo = []
    localMaximum = 0
    allPossible2DiceKept = checkForIdenticPairs(combination, 2)
    for pKD1, pKD2 in allPossible2DiceKept:
        savedDice = [combination[pKD1], combination[pKD2]]
        outcomeTwo = list(generateRolls(3))
        totalScore = 0
        for finalCombination in outcomeTwo:
            finalCombination.append(savedDice[0])
            finalCombination.append(savedDice[1])
            if halfFull == 1:
                provKey = createTableKey(finalCombination)
                totalScore += tableValues[provKey][0]
            else:
                score, _ = checkScore(finalCombination)
                totalScore += score
        
        totalScore = totalScore / len(outcomeTwo)
        if totalScore > localMaximum:
            localMaximum = totalScore
            listOfDicePositions[1] = list([pKD1, pKD2])
    
    return localMaximum

def uniqueCombinationDice3(combination, halfFull):
    outcomeThree = []
    localMaximum = 0
    allPossible3DiceKept = checkForIdenticPairs(combination, 3)
    for pKD1, pKD2, pKD3 in allPossible3DiceKept:
        savedDice = [combination[pKD1], combination[pKD2], combination[pKD3]]
        outcomeThree = list(generateRolls(2))
        totalScore = 0
        for finalCombination in outcomeThree:
            finalCombination.append(savedDice[0])
            finalCombination.append(savedDice[1])
            finalCombination.append(savedDice[2])
            if halfFull == 1:
                provKey = createTableKey(finalCombination)
                totalScore += tableValues[provKey][0]
            else:
                score, _ = checkScore(finalCombination)
                totalScore += score
        
        totalScore = totalScore / len(outcomeThree)
        if totalScore > localMaximum:
            localMaximum = totalScore
            listOfDicePositions[2] = list([pKD1, pKD2, pKD3])
            
    return localMaximum

def uniqueCombinationDice4(combination, halfFull):
    outcomeFour = []
    localMaximum = 0
    allPossible4DiceKept = checkForIdenticPairs(combination, 4)
    for pKD1, pKD2, pKD3, pKD4 in allPossible4DiceKept:
        partialCombination = [combination[pKD1], combination[pKD2], combination[pKD3], combination[pKD4], 0]
        outcomeFour = list(generateRolls(1))
        totalScore = 0
        for finalDice in outcomeFour:
            partialCombination[4] = finalDice[0]
            if halfFull == 1:
                provKey = createTableKey(partialCombination)
                totalScore += tableValues[provKey][0]
            else:
                score, _ = checkScore(partialCombination)
                totalScore += score
        
        totalScore = totalScore / len(outcomeFour)
        if totalScore > localMaximum:
            localMaximum = totalScore
            #print(pKD1, pKD2, pKD3, pKD4)
            listOfDicePositions[3] = list([pKD1, pKD2, pKD3, pKD4])
              
    return localMaximum        
        
    
def expectiMax(combination):
    defaultScore, _ = checkScore(combination)
    numberOfDices = 0
    expectiMaxScore = [0] * 6
    expectiMaxScore[-1] = defaultScore
    for noOfDicesKept in range(5):
        if noOfDicesKept == 0:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice0(combination, 1)
        elif noOfDicesKept == 1:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice1(combination, 1)
        elif noOfDicesKept == 2:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice2(combination, 1)
        elif noOfDicesKept == 3:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice3(combination, 1)
        elif noOfDicesKept == 4:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice4(combination, 1)
                  
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


def halfExpectiMax(combination):
    defaultScore, _ = checkScore(combination)
    dicesToBeKept = 0
    expectiMaxScore = [0] * 6
    expectiMaxScore[-1] = defaultScore
    for noOfDicesKept in range(5):
        if noOfDicesKept == 0:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice0(combination, 0)
        elif noOfDicesKept == 1:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice1(combination, 0)
        elif noOfDicesKept == 2:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice2(combination, 0)
        elif noOfDicesKept == 3:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice3(combination, 0)
        elif noOfDicesKept == 4:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice4(combination, 0)
    
    for dice, score in enumerate(expectiMaxScore):
        if score >= defaultScore:
            defaultScore = score
            dicesToBeKept = dice
    
    return defaultScore, dicesToBeKept


def playExpectiMax(combination):
    defaultScore, _ = checkScore(combination)
    dicesToBeKept = 0
    expectiMaxScore = [0] * 6
    expectiMaxScore[-1] = defaultScore
    for noOfDicesKept in range(5):
        if noOfDicesKept == 0:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice0(combination, 1)
        elif noOfDicesKept == 1:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice1(combination, 1)
        elif noOfDicesKept == 2:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice2(combination, 1)
        elif noOfDicesKept == 3:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice3(combination, 1)
        elif noOfDicesKept == 4:
            expectiMaxScore[noOfDicesKept] = uniqueCombinationDice4(combination, 1)
                  
    
    for dice, score in enumerate(expectiMaxScore):
        if score >= defaultScore:
            defaultScore = score
            dicesToBeKept = dice
    
    return defaultScore, dicesToBeKept
            

def playYahtzee():
    yourCombination = []
    rd.seed()
    for i in range(5):
        yourCombination.append(rd.randint(1,6))
        
    print("Your starting dices are : ",yourCombination)
    yourScore, combKey = checkScore(yourCombination)
    print("Your score right now is : ", yourScore, "you hit: ", combinationName.get(combKey))
    
    bestScore, dices = playExpectiMax(yourCombination)
    
    if dices == 0:
        print("Best move is to roll all dices, with an expectiMax score of : ", bestScore)
    elif dices == 5:
        print("Best move is to keep all dices, with an expectiMax score of : ", bestScore)
    else:
        print("Best move is to keep the dices in the following positions : ", listOfDicePositions[dices - 1], " with an expectiMax score of : ", bestScore)
    
    yourNewCombination = []
    for i in listOfDicePositions[dices - 1]:
        yourNewCombination.append(yourCombination[i])
    
    newRandoms = 5 - len(yourNewCombination)
    for i in range(newRandoms):
        yourNewCombination.append(rd.randint(1,6))
    
    
    print("-----------------You roll-----------------")
    print("Your new dices are : ", yourNewCombination)
    yourScore, combKey = checkScore(yourNewCombination)
    print("Your score now is : ", yourScore, "because you hit : ", combinationName.get(combKey))
   
   
    #print("------------------------------", listOfDicePositions, "-------------------------------") 
    bestScore, dices = halfExpectiMax(yourNewCombination)
    #print("------------------------------", listOfDicePositions, "-------------------------------") 

    if dices == 0:
        print("Best move is to roll all dices, with an expectiMax score of : ", bestScore)
    elif dices == 5:
        _,combKey = checkScore(yourNewCombination)
        print("Best move is to keep all dices, with an expectiMax score of : ", bestScore, "and you hit : ", combinationName.get(combKey))
        return 0   
    else:
        print("Best move is to keep the dices in the following positions : ", listOfDicePositions[dices - 1], " with an expectiMax score of : ", bestScore)
    
    
    yourCombination = yourNewCombination
    yourNewCombination = []
    for i in listOfDicePositions[dices - 1]:
        yourNewCombination.append(yourCombination[i])
    
    newRandoms = 5 - len(yourNewCombination)
    for i in range(newRandoms):
        yourNewCombination.append(rd.randint(1,6))
    
    print("-----------------You roll-----------------")
    print("Your new dices are : ", yourNewCombination)
    yourScore, combKey = checkScore(yourNewCombination)
    print("Your FINAL score is : ", yourScore, " and you hit : ", combinationName.get(combKey))


playYahtzee()

#ChooseCombination = [6,6,6,6,1]
ChooseCombination = [2,1,5,2,2]


#print("-------------11111111----------", allPossible1DiceKept)
#print("-------------22222222----------", allPossible2DiceKept)
#print("-------------33333333----------", allPossible3DiceKept)
#print("-------------44444444----------", allPossible4DiceKept)



#checkScore(ChooseCombination)
#print(expectiMax(ChooseCombination))-
        


            


