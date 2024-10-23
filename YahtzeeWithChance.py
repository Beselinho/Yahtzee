import csv
import random as rd
import ast
import numpy as np

#scores caluculated based on the percentage they provided to reach the treeshold of 63 points
ONES_SCORE = 4.66
TWOS_SCORE = 9.33  
THREES_SCORE = 13.99
FOURS_SCORE = 18.66
FIVES_SCORE = 23.33
SIXES_SCORE = 27.975
AVERAGE_THREE_OF_A_KIND_SCORE = 18
AVERAGE_FOUR_OF_A_KIND_SCORE = 18
FULL_HOUSE_SCORE = 25
SMALL_STRAIGHT_SCORE = 30
LARGE_STRAIGHT_SCORE = 40
YATHZEE_SCORE = 50

combinationNames = [
        " ","Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
        "ToaK", "FoaK", "FH", "SS", "LS", "Yathzee", "Chance"
    ]

filenameOnes = "CSV_Tables/TableOnes.csv"
filenameTwos = "CSV_Tables/TableTwos.csv"
filenameThrees =  "CSV_Tables/TableThrees.csv"
filenameFours = "CSV_Tables/TableFours.csv"
filenameFives = "CSV_Tables/TableFives.csv"
filenameSixes = "CSV_Tables/TableSixes.csv"
filenameToaK = "CSV_Tables/TableToaK.csv"
filenameFoaK = "CSV_Tables/TableFoaK.csv"
filenameFH = "CSV_Tables/TableFH.csv"
filenameSS = "CSV_Tables/TableSS.csv"
filenameLS = "CSV_Tables/TableLS.csv"
filenameYathzee = "CSV_Tables/TableYathzee.csv"

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
            oneActionChance = float(row['OneChance'])
            oneActionKeptPositions = ast.literal_eval(row['OneKeptPositions'])
            twoActionChance = float(row['TwoChance'])
            twoActionKeptPositions = ast.literal_eval(row['TwoKeptPositions'])
            
            tableChances[key] = {
                'OneActionChance': oneActionChance,
                'OneActionKeptPositions': oneActionKeptPositions,
                'TwoActionChance': twoActionChance,
                'TwoActionKeptPositions': twoActionKeptPositions
            }
    
    return tableChances

tableChancesOnes = readCSVFile(filenameOnes)
tableChancesTwos = readCSVFile(filenameTwos)
tableChancesThrees = readCSVFile(filenameThrees)
tableChancesFours = readCSVFile(filenameFours)
tableChancesFives = readCSVFile(filenameFives)
tableChancesSixes = readCSVFile(filenameSixes)
tableChancesToaK = readCSVFile(filenameToaK)
tableChancesFoaK = readCSVFile(filenameFoaK)
tableChancesFH = readCSVFile(filenameFH)
tableChancesSS = readCSVFile(filenameSS)
tableChancesLS = readCSVFile(filenameLS)
tableChancesYathzee = readCSVFile(filenameYathzee)

# scoreboard = {
#     "Ones": -1,
#     "Twos": -1,
#     "Threes": -1,
#     "Fours": -1,
#     "Fives": -1,
#     "Sixes": -1,
#     "ToaK": -1,
#     "FoaK": -1,
#     "FH": -1,
#     "SS": -1,
#     "LS": -1,
#     "Yathzee": -1,
#     "chance" : -1
# }
#             0,1,2,3,4,5,6,7,8,9,10,11,12,13      
#scoreboard = [0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
#scoreboard declarat aici

def determineScore(combination, scoreboard):
    combination.sort()
    score = 0
    localScore = 0
    hit = 0
    freqVector = [0] * 6
    
    for die in combination:
        freqVector[die - 1] += 1
    
    if scoreboard[1] == -1:
        #Ones
        localScore = freqVector[0] * 1
        if (localScore > score):
            score = localScore
            hit = 1
    if scoreboard[2] == -1:
        #Twos
        localScore = freqVector[1] * 2
        if (localScore > score):
            score = localScore
            hit = 2
    if scoreboard[3] == -1:
        #Threes
        localScore = freqVector[2] * 3
        if (localScore > score):
            score = localScore
            hit = 3
    if scoreboard[4] == -1:
        #Fours
        localScore = freqVector[3] * 4
        if (localScore > score):
            score = localScore
            hit = 4
    if scoreboard[5] == -1:
        #Fives
        localScore = freqVector[4] * 5
        if (localScore > score):
            score = localScore
            hit = 5
    if scoreboard[6] == -1:
        #Sixes
        localScore = freqVector[5] * 6
        #print("localScore", localScore)
        if (localScore > score):
            score = localScore
            hit = 6
    if scoreboard[7] == -1:
        #Three of a Kind
        for no in freqVector:
            if no >= 3:
                localScore = sum(combination)
                #print("localScore", localScore)
                if (localScore > score):
                    score = localScore
                    hit = 7
    if scoreboard[8] == -1:
        #Four of a Kind
        for no in freqVector:
            if no >= 4:
                localScore = sum(combination)
                #print("localScore", localScore)
                if (localScore > score):
                    score = localScore
                    hit = 8
    if scoreboard[9] == -1:
        #Full House
        sortedFreq = sorted(freqVector)
        if sortedFreq[-1] == 3 and sortedFreq[-2] == 2:
            localScore = FULL_HOUSE_SCORE
            #print("localScore", localScore)
            if (localScore > score):
                score = localScore
                hit = 9
    if scoreboard[10] == -1:
        #Small Straight
        if((freqVector[0] >= 1 and freqVector[1] >= 1 and freqVector[2] >= 1 and freqVector[3] >= 1) or (freqVector[1] >= 1 and freqVector[2] >= 1 and freqVector[3] >= 1 and freqVector[4] >= 1)
        or (freqVector[2] >= 1 and freqVector[3] >= 1 and freqVector[4] >= 1 and freqVector[5] >= 1)):
                localScore = SMALL_STRAIGHT_SCORE
                #print("localScore", localScore)
                if (localScore > score):
                    score = localScore
                    hit = 10
    if scoreboard[11] == -1:
        # Large Straight
        auxCombination = combination.copy()
        auxCombination.sort()
        largeSequence1 = [1,2,3,4,5]
        largeSequence2 = [2,3,4,5,6]
        if auxCombination == largeSequence1 or auxCombination == largeSequence2:
            localScore = LARGE_STRAIGHT_SCORE
            #print("localScore", localScore)
            if (localScore > score):
                score = localScore
                hit = 11
    if scoreboard[13] == -1:
        #Chance
        localScore = sum(combination)
        #print("localScore", localScore)
        if localScore > score:
            score = localScore
            hit = 13
            
    #Yathzee
    for no in freqVector:
        if no == 5:
            localScore = YATHZEE_SCORE
            #print("localScore", localScore)
            if (localScore > score):
                score = localScore
            hit = 12
            
    return score, hit
    

def checkThreeOfAKind(combination):
    freqVector = [0] * 6
    for die in combination:
        freqVector[die - 1] += 1
    for no in freqVector:
        if no >= 3:
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

def checkLargeStraight(combination):
    auxCombination = combination.copy()
    auxCombination.sort()
    largeSequence1 = [1,2,3,4,5]
    largeSequence2 = [2,3,4,5,6]
    if auxCombination == largeSequence1 or auxCombination == largeSequence2:
        return True
    return False

def checkYathzee(combination):
    freqVector = [0] * 6
    for die in combination:
        freqVector[die - 1] += 1
    for no in freqVector:
        if no == 5:
            return True
    return False

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

def createTableKey(combination):
    freqVector = [0] * 6
    for diceFace in combination:
      freqVector[diceFace - 1] += 1
    
    key = ''.join(str(freqVector[i]) for i in range(len(freqVector)))
    return key  

def rollDice(num_dice):
    rd.seed()
    return [rd.randint(1, 6) for _ in range(num_dice)]

def calculateExpectedValue(chance, score):
    return chance * score

def playRound(scoreboard):
    initialRoll = rollDice(5)
    initialRoll.sort()
    #print("Initial Roll :", initialRoll)
    tableKey1 = createTableKey(initialRoll)
   
    
    bestExpected1 = [0] * 14
    bestExpected1Postions = [0] * 14 
    for index in range(1, len(scoreboard)):
        if scoreboard[index] == -1:
            if index == 1:
                bestExpected1[index] = calculateExpectedValue(tableChancesOnes[tableKey1]['TwoActionChance'], ONES_SCORE)
                bestExpected1Postions[index] = tableChancesOnes[tableKey1]['TwoActionKeptPositions']
            elif index == 2:
                bestExpected1[index] = calculateExpectedValue(tableChancesTwos[tableKey1]['TwoActionChance'], TWOS_SCORE)
                bestExpected1Postions[index] = tableChancesTwos[tableKey1]['TwoActionKeptPositions']
            elif index == 3:
                bestExpected1[index] = calculateExpectedValue(tableChancesThrees[tableKey1]['TwoActionChance'], THREES_SCORE)
                bestExpected1Postions[index] = tableChancesThrees[tableKey1]['TwoActionKeptPositions']
            elif index == 4:
                bestExpected1[index] = calculateExpectedValue(tableChancesFours[tableKey1]['TwoActionChance'], FOURS_SCORE)
                bestExpected1Postions[index] = tableChancesFours[tableKey1]['TwoActionKeptPositions']
            elif index == 5:
                bestExpected1[index] = calculateExpectedValue(tableChancesFives[tableKey1]['TwoActionChance'], FIVES_SCORE)
                bestExpected1Postions[index] = tableChancesFives[tableKey1]['TwoActionKeptPositions']
            elif index == 6:
                bestExpected1[index] = calculateExpectedValue(tableChancesSixes[tableKey1]['TwoActionChance'], SIXES_SCORE)
                bestExpected1Postions[index] = tableChancesSixes[tableKey1]['TwoActionKeptPositions']
            elif index == 7:
                bestExpected1[index] = calculateExpectedValue(tableChancesToaK[tableKey1]['TwoActionChance'], AVERAGE_THREE_OF_A_KIND_SCORE)
                bestExpected1Postions[index] = tableChancesToaK[tableKey1]['TwoActionKeptPositions']
            elif index == 8:
                bestExpected1[index] = calculateExpectedValue(tableChancesFoaK[tableKey1]['TwoActionChance'], AVERAGE_FOUR_OF_A_KIND_SCORE)
                bestExpected1Postions[index] = tableChancesFoaK[tableKey1]['TwoActionKeptPositions']
            elif index == 9:
                bestExpected1[index] = calculateExpectedValue(tableChancesFH[tableKey1]['TwoActionChance'], FULL_HOUSE_SCORE)
                bestExpected1Postions[index] = tableChancesFH[tableKey1]['TwoActionKeptPositions']
            elif index == 10:
                bestExpected1[index] = calculateExpectedValue(tableChancesSS[tableKey1]['TwoActionChance'], SMALL_STRAIGHT_SCORE)
                bestExpected1Postions[index] = tableChancesSS[tableKey1]['TwoActionKeptPositions']
            elif index == 11:
                bestExpected1[index] = calculateExpectedValue(tableChancesLS[tableKey1]['TwoActionChance'], LARGE_STRAIGHT_SCORE)
                bestExpected1Postions[index] = tableChancesLS[tableKey1]['TwoActionKeptPositions']
            elif index == 12:
                bestExpected1[index] = calculateExpectedValue(tableChancesYathzee[tableKey1]['TwoActionChance'], YATHZEE_SCORE)
                bestExpected1Postions[index] = tableChancesYathzee[tableKey1]['TwoActionKeptPositions']
            elif index == 13:
                bestExpected1[index] = sum(initialRoll)
                bestExpected1Postions[index] = [0,1,2,3,4]
            else:
                break
    
    
    reversedBestExpected1 = bestExpected1[::-1]
    reversedBestExpected1Positions = bestExpected1Postions[::-1]
    highestExpectedIdx1 = np.argmax(reversedBestExpected1)        
    # if reversedBestExpected1[13] < 20:
    #     highestExpectedIdx1 = np.argmax(reversedBestExpected1[1:12])
    # else:
    #     highestExpectedIdx1 = 13
    highestExpectedPositionIdx1 = reversedBestExpected1Positions[highestExpectedIdx1]
    
    # print("------1st------",bestExpected1)
    # print("------1st------",bestExpected1Postions)
    # print("------1stCombo------",13 - highestExpectedIdx1)
    # print("------1stPositions------",highestExpectedPositionIdx1)
    
    firstRoll = []
    if isinstance(highestExpectedPositionIdx1, list) and len(highestExpectedPositionIdx1) != 0:
        for i in highestExpectedPositionIdx1:
            firstRoll.append(initialRoll[i])
    nextRoll = rollDice(5 - len(firstRoll))
    for i in range(len(nextRoll)):
        firstRoll.append(nextRoll[i])
        
    firstRoll.sort() 
    #print("Your Dices after the first roll : ",firstRoll)
    
    
    tableKey2 = createTableKey(firstRoll)
   
    
    bestExpected2 = [0] * 14
    bestExpected2Postions = [0] * 14 
    for index in range(1, len(scoreboard)):
        if scoreboard[index] == -1:
            if index == 1:
                bestExpected2[index] = calculateExpectedValue(tableChancesOnes[tableKey2]['OneActionChance'], ONES_SCORE)
                bestExpected2Postions[index] = tableChancesOnes[tableKey2]['OneActionKeptPositions']
            elif index == 2:
                bestExpected2[index] = calculateExpectedValue(tableChancesTwos[tableKey2]['OneActionChance'], TWOS_SCORE)
                bestExpected2Postions[index] = tableChancesTwos[tableKey2]['OneActionKeptPositions']
            elif index == 3:
                bestExpected2[index] = calculateExpectedValue(tableChancesThrees[tableKey2]['OneActionChance'], THREES_SCORE)
                bestExpected2Postions[index] = tableChancesThrees[tableKey2]['OneActionKeptPositions']
            elif index == 4:
                bestExpected2[index] = calculateExpectedValue(tableChancesFours[tableKey2]['OneActionChance'], FOURS_SCORE)
                bestExpected2Postions[index] = tableChancesFours[tableKey2]['OneActionKeptPositions']
            elif index == 5:
                bestExpected2[index] = calculateExpectedValue(tableChancesFives[tableKey2]['OneActionChance'], FIVES_SCORE)
                bestExpected2Postions[index] = tableChancesFives[tableKey2]['OneActionKeptPositions']
            elif index == 6:
                bestExpected2[index] = calculateExpectedValue(tableChancesSixes[tableKey2]['OneActionChance'], SIXES_SCORE)
                bestExpected2Postions[index] = tableChancesSixes[tableKey2]['OneActionKeptPositions']
            elif index == 7:
                bestExpected2[index] = calculateExpectedValue(tableChancesToaK[tableKey2]['OneActionChance'], AVERAGE_THREE_OF_A_KIND_SCORE)
                bestExpected2Postions[index] = tableChancesToaK[tableKey2]['OneActionKeptPositions']
            elif index == 8:
                bestExpected2[index] = calculateExpectedValue(tableChancesFoaK[tableKey2]['OneActionChance'], AVERAGE_FOUR_OF_A_KIND_SCORE)
                bestExpected2Postions[index] = tableChancesFoaK[tableKey2]['OneActionKeptPositions']
            elif index == 9:
                bestExpected2[index] = calculateExpectedValue(tableChancesFH[tableKey2]['OneActionChance'], FULL_HOUSE_SCORE)
                bestExpected2Postions[index] = tableChancesFH[tableKey2]['OneActionKeptPositions']
            elif index == 10:
                bestExpected2[index] = calculateExpectedValue(tableChancesSS[tableKey2]['OneActionChance'], SMALL_STRAIGHT_SCORE)
                bestExpected2Postions[index] = tableChancesSS[tableKey2]['OneActionKeptPositions']
            elif index == 11:
                bestExpected2[index] = calculateExpectedValue(tableChancesLS[tableKey2]['OneActionChance'], LARGE_STRAIGHT_SCORE)
                bestExpected2Postions[index] = tableChancesLS[tableKey2]['OneActionKeptPositions']
            elif index == 12:
                bestExpected2[index] = calculateExpectedValue(tableChancesYathzee[tableKey2]['OneActionChance'], YATHZEE_SCORE)
                bestExpected2Postions[index] = tableChancesYathzee[tableKey2]['OneActionKeptPositions']
            elif index == 13:
                bestExpected2[index] = sum(firstRoll)
                bestExpected2Postions[index] = [0,1,2,3,4]
            else:
                break
            
    reversedBestExpected2 = bestExpected2[::-1]
    reversedBestExpected2Positions = bestExpected2Postions[::-1]
    highestExpectedIdx2 = np.argmax(reversedBestExpected2)
    # if reversedBestExpected2[13] < 20:
    #     highestExpectedIdx2 = np.argmax(reversedBestExpected2[1:12])
    # else:
    #     highestExpectedIdx2 = 13
    highestExpectedPositionIdx2 = reversedBestExpected2Positions[highestExpectedIdx2]
    
    # print("------2nd--------",bestExpected2)
    # print("------2nd------",bestExpected2Postions)
    # print("------2ndCombo-----",13 - highestExpectedIdx2)
    # print("------2ndPositions------",highestExpectedPositionIdx2)
    
    secondRoll = [firstRoll[i] for i in highestExpectedPositionIdx2]
    randomThing = 0
    if len(secondRoll) == 5:
        #print("No more sense for rolling")
        randomThing += 1
    else:
        nextRoll = rollDice(5 - len(secondRoll))
        secondRoll.extend(nextRoll)
     
    secondRoll.sort()   
    #print("Your Dices after the second roll : ",secondRoll)
    
    
    roundScore, hit = determineScore(secondRoll, scoreboard)
    
    secondYahtzee = False
    if hit == 12:
        secondYahtzee = True
        if scoreboard[hit] == YATHZEE_SCORE:
            scoreboard[0] += 100
            #if second yahtzee is scored, the player gets bonus 100 points and can score in any category he wants.
            if scoreboard[secondRoll[0]] == -1:
                scoreboard[secondRoll[0]] = sum(secondRoll)
            elif scoreboard[7] == -1:
                scoreboard[7] = sum(secondRoll)
            elif scoreboard[8] == -1:
                scoreboard[8] = sum(secondRoll)
            elif scoreboard[9] == -1:
                scoreboard[9] = FULL_HOUSE_SCORE
            elif scoreboard[10] == -1:
                scoreboard[10] = SMALL_STRAIGHT_SCORE
            elif scoreboard[11] == -1:
                scoreboard[11] = LARGE_STRAIGHT_SCORE
            else:
                scoreboard[np.argmin(scoreboard)] = 0
        else:
            scoreboard[hit] = YATHZEE_SCORE
            
    if not secondYahtzee:           
        if roundScore != 0:
            scoreboard[hit] = roundScore
        else:
            scoreboard[np.argmin(scoreboard)] = 0
    
    # print("Scoreboard after the round",scoreboard)
    # print("Score for the round",roundScore)
    # print("Hit:", hit)
    
def playFullGame(numSimuations, scoreboard):       
    averageScore = 0
    upperScore = 0
    goodScore = 0
    badScore = 0
    greatScore = 0
    index = 0
    while index < numSimuations:
        if index % 10000 == 0:
            print(index)
        totalScore = 0
        scoreboard = [0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        for i in range(13):
            #print("Round ", i + 1)
            playRound(scoreboard)
        
        # for i in range(1, len(scoreboard)):
        #     print(f"{combinationNames[i]} : {scoreboard[i]}")
        
        totalScore = sum(scoreboard)
        for i in range(1,7):
            upperScore += scoreboard[i]
        if upperScore >= 63:
            totalScore += 35
            
        #print("Total Score: ", totalScore)
        if totalScore < 250:
            badScore += 1
        elif totalScore >= 250 and totalScore <= 280:
            goodScore += 1
        else:
            greatScore += 1
        averageScore += totalScore
        scoreVector.append(totalScore)
        index += 1
    
    print("Average Score:", averageScore / numSimuations, "per 100000 games")
    #print("Times it got a bad score :", badScore, "Times it got a good score :", goodScore, "Times it got a great score :", greatScore)
    #print("Score Vector: ", scoreVector)

def mePlayYahtzee(scoreboard):
    initialRoll = rollDice(5)
    print("Initial Roll :", initialRoll)

    print("Select the positions of the dice you want to keep (1-5) separated by spaces, or type 0 to keep all")
    keptDice = input().split()
    if '0' in keptDice:
        firstRoll = initialRoll
    else:
        keptDice = [int(pos) - 1 for pos in keptDice if pos.isdigit() and 0 < int(pos) <= 5]
        print("You chose to keep these dice:", [initialRoll[pos] for pos in keptDice])

        numToRoll = 5 - len(keptDice)
        firstRoll = rollDice(numToRoll)
        for pos in keptDice:
            firstRoll.append(initialRoll[pos])
    print("Your Dice after the first roll:", firstRoll)

    print("Select the positions of the dice you want to keep (1-5) separated by spaces, or type 0 to keep all")
    keptDice = input().split()
    if '0' in keptDice:
        secondRoll = firstRoll
    else:
        keptDice = [int(pos) - 1 for pos in keptDice if pos.isdigit() and 0 < int(pos) <= 5]
        print("You chose to keep these dice:", [firstRoll[pos] for pos in keptDice])

        numToRoll = 5 - len(keptDice)
        secondRoll = rollDice(numToRoll)
        for pos in keptDice:
            secondRoll.append(firstRoll[pos])
    print("Your Dice after the second roll:", secondRoll)

    ok = False
    print("These are category codes : 1.Ones  2.Twos  3.Threes  4.Fours  5.Fives  6.Sixes 7.ToaK  8.FoaK  9.FH  10.SS  11.LS  12.Yahtzee  13.Chance")
    print("Choose in which category you want to score :")
    while not ok:
        userChoice = int(input())
        if scoreboard[userChoice] == -1:
            ok = True
            if userChoice == 1:
                scoreboard[userChoice] = sum(dice for dice in secondRoll if dice == 1)
            elif userChoice == 2:
                scoreboard[userChoice] = sum(dice for dice in secondRoll if dice == 2)
            elif userChoice == 3:
                scoreboard[userChoice] = sum(dice for dice in secondRoll if dice == 3)
            elif userChoice == 4:
                scoreboard[userChoice] = sum(dice for dice in secondRoll if dice == 4)
            elif userChoice == 5:
                scoreboard[userChoice] = sum(dice for dice in secondRoll if dice == 5)
            elif userChoice == 6:
                scoreboard[userChoice] = sum(dice for dice in secondRoll if dice == 6)
            elif userChoice == 7:
                if checkThreeOfAKind(secondRoll):
                    scoreboard[userChoice] = sum(secondRoll)
                else:
                    scoreboard[userChoice] = 0
            elif userChoice == 8:
                if checkFourOfAKind(secondRoll):
                    scoreboard[userChoice] = sum(secondRoll)
                else:
                    scoreboard[userChoice] = 0
            elif userChoice == 9:
                if checkFullHouse(secondRoll):
                    scoreboard[userChoice] = FULL_HOUSE_SCORE
                else:
                    scoreboard[userChoice] = 0
            elif userChoice == 10:
                if checkSmallStraight(secondRoll):
                    scoreboard[userChoice] = SMALL_STRAIGHT_SCORE
                else:
                    scoreboard[userChoice] = 0
            elif userChoice == 11:
                if checkLargeStraight(secondRoll):
                    scoreboard[userChoice] = LARGE_STRAIGHT_SCORE
                else:
                    scoreboard[userChoice] = 0
            elif userChoice == 12:
                if checkYathzee(secondRoll):
                    scoreboard[userChoice] = YATHZEE_SCORE
                else:
                    scoreboard[userChoice] = 0
            elif userChoice == 13:
                scoreboard[userChoice] = sum(secondRoll)
        else:
            print("Category already scored, please choose another one")
    
    print("Scoreboard after your round:")
    for i in range(1, len(scoreboard)):
        print(f"{combinationNames[i]} : {scoreboard[i]}")
        

def mePlayFullYahtzee(scoreboard):
    for i in range(13):
        print("Round ", i + 1)
        mePlayYahtzee(scoreboard)

    print("Final Score:" , sum(scoreboard))
    
    
    

scoreboard = [0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
scoreVector = []
numSimulations = 100000 
playFullGame(numSimulations, scoreboard)
#mePlayFullYahtzee(scoreboard) 
#print(scoreVector)
