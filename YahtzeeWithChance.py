import csv
import random as rd
import ast
import os

FULL_HOUSE_SCORE = 25
SMALL_STRAIGHT_SCORE = 30

# base_dir = os.path.dirname(__file__)
# csv_dir = os.path.join(base_dir,'CSV_Tabels')  # '..' to go up one directory

# Full paths to the specific CSV files
filenameFH = "tableChanceForFH.csv"
filenameSS = "tableChanceForSS.csv"

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


tableChancesFH = readCSVFile(filenameFH)
tableChancesSS = readCSVFile(filenameSS)

def checkFullHouse(combination):
    freqVector = [0] * 7
    for die in combination:
        freqVector[die] += 1
    sortedFreq = sorted(freqVector)
    return sortedFreq[-1] == 3 and sortedFreq[-2] == 2

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

def calculateInitialScore(yourCombination, FHS, SSS):
    if checkFullHouse(yourCombination) and FHS == 0:
        return FULL_HOUSE_SCORE
    elif checkSmallStraight(yourCombination) and SSS == 0:
        return SMALL_STRAIGHT_SCORE
    else:
        return 

def bestAction(combination, table, actionsLeft):
    keptPositions = []
    chance = 0
    field = "One" if actionsLeft == 1 else "Two"
    key = createTableKey(combination)
    if key in table:
        chance = table[key][field + 'ActionChance']
        keptPositions = table[key][field + 'ActionKeptPositions']
    return chance, keptPositions

def executeRoll(kept_positions, combination):
    new_combination = [combination[i] for i in kept_positions]
    num_new_rolls = 5 - len(new_combination)
    new_combination.extend(rollDice(num_new_rolls))
    new_combination.sort()
    return new_combination

def performRoll(yourCombination, tableChancesFH, tableChancesSS, FHS, SSS, rollNum):
    fhChance, fhKeptPositions = bestAction(yourCombination, tableChancesFH, rollNum)
    ssChance, ssKeptPositions = bestAction(yourCombination, tableChancesSS, rollNum)

    fhChance = 0 if FHS else fhChance
    ssChance = 0 if SSS else ssChance

    if fhChance > ssChance:
        yourCombination = executeRoll(fhKeptPositions, yourCombination)
    else:
        yourCombination = executeRoll(ssKeptPositions, yourCombination)
    
    return yourCombination

def performRollForValue(yourCombination, tableChancesFH, tableChancesSS, FHS, SSS, rollNum):
    fhChance, fhKeptPositions = bestAction(yourCombination, tableChancesFH, rollNum)
    ssChance, ssKeptPositions = bestAction(yourCombination, tableChancesSS, rollNum)

    fhChance = 0 if FHS else fhChance
    ssChance = 0 if SSS else ssChance

    if calculateExpectedValue(fhChance, FULL_HOUSE_SCORE) > calculateExpectedValue(ssChance, SMALL_STRAIGHT_SCORE):
        yourCombination = executeRoll(fhKeptPositions, yourCombination)
    else:
        yourCombination = executeRoll(ssKeptPositions, yourCombination)
    
    return yourCombination

def playRoundAlwaysRollAll():
    yourCombination = rollDice(5)
   # print(f"Initial Roll: {yourCombination}")
    yourCombination.sort()

    if checkFullHouse(yourCombination):
        #print("You got a Full House!")
        return FULL_HOUSE_SCORE
    elif checkSmallStraight(yourCombination):
        #print("You got a Small Straight!")
        return SMALL_STRAIGHT_SCORE

    yourCombination = rollDice(5)
    #print(f"Second Roll: {yourCombination}")
    yourCombination.sort()

    if checkFullHouse(yourCombination):
        #print("You got a Full House!")
        return FULL_HOUSE_SCORE
    elif checkSmallStraight(yourCombination):
        #print("You got a Small Straight!")
        return SMALL_STRAIGHT_SCORE
    else:
        #print("You got nothing
        return 0

def playRoundRandomFirstRoll(tableChancesFH, tableChancesSS, FHS, SSS):
    yourCombination = rollDice(5)
   # print(f"Initial Roll: {yourCombination}")
    yourCombination.sort()

    if checkFullHouse(yourCombination) and FHS == 0:
        #print("You got a Full House!")
        return FULL_HOUSE_SCORE
    elif checkSmallStraight(yourCombination) and SSS == 0:
        #print("You got a Small Straight!")
        return SMALL_STRAIGHT_SCORE

    fhChance, fhKeptPositions = bestAction(yourCombination, tableChancesFH, 1)
    ssChance, ssKeptPositions = bestAction(yourCombination, tableChancesSS, 1)
    
    fhChance = 0 if FHS else fhChance
    ssChance = 0 if SSS else ssChance

    if fhChance > ssChance and FHS == 0:
        yourCombination = executeRoll(fhKeptPositions, yourCombination)
        if checkFullHouse(yourCombination):
            #print("You got a Full House!")
            return FULL_HOUSE_SCORE
        elif checkSmallStraight(yourCombination):
            #print("You got a Small Straight!")
            return SMALL_STRAIGHT_SCORE
    else:
        yourCombination = executeRoll(ssKeptPositions, yourCombination)
        if checkSmallStraight(yourCombination):
            #print("You got a Small Straight!")
            return SMALL_STRAIGHT_SCORE
        elif checkFullHouse(yourCombination):
            #print("You got a Full House!")
            return FULL_HOUSE_SCORE

    return 0

def playRoundYourStrategy(tableChancesFH, tableChancesSS, FHS, SSS):
    yourCombination = rollDice(5)
    yourCombination.sort()
    
    score = calculateInitialScore(yourCombination, FHS, SSS)
    alreadyHit = 1 if score else 0

    if not alreadyHit:
        yourCombination = performRoll(yourCombination, tableChancesFH, tableChancesSS, FHS, SSS, 0)

        if checkFullHouse(yourCombination):
            score = FULL_HOUSE_SCORE
        elif checkSmallStraight(yourCombination):
            score = SMALL_STRAIGHT_SCORE
        else:
            yourCombination = performRoll(yourCombination, tableChancesFH, tableChancesSS, FHS, SSS, 1)
            
            if checkFullHouse(yourCombination):
                score = FULL_HOUSE_SCORE
            elif checkSmallStraight(yourCombination):
                score = SMALL_STRAIGHT_SCORE
            else:
                score = 0

    return score

def calculateExpectedValue(chance, score):
    return chance * score

def playRoundYourStrategyValue(tableChancesFH, tableChancesSS, FHS, SSS):
    yourCombination = rollDice(5)
    yourCombination.sort()
    
    score = calculateInitialScore(yourCombination, FHS, SSS)
    alreadyHit = 1 if score else 0

    if not alreadyHit:
        yourCombination = performRollForValue(yourCombination, tableChancesFH, tableChancesSS, FHS, SSS, 0)

        if checkFullHouse(yourCombination):
            score = FULL_HOUSE_SCORE
        elif checkSmallStraight(yourCombination):
            score = SMALL_STRAIGHT_SCORE
        else:
            yourCombination = performRollForValue(yourCombination, tableChancesFH, tableChancesSS, FHS, SSS, 1)
            
            if checkFullHouse(yourCombination):
                score = FULL_HOUSE_SCORE
            elif checkSmallStraight(yourCombination):
                score = SMALL_STRAIGHT_SCORE
            else:
                score = 0

    return score


def playGame(tableChancesFH, tableChancesSS, strategy):
    total_score = 0
    fhScoreObtained = False
    ssScoreObtained = False

    for round_number in range(1, 3):
        #print(f"Round {round_number}:")
        if strategy == 'always_roll_all':
            roundScore = playRoundAlwaysRollAll()
        elif strategy == 'random_first_roll':
            roundScore = playRoundRandomFirstRoll(tableChancesFH, tableChancesSS, fhScoreObtained, ssScoreObtained)
        elif strategy == 'highest_chance_strategy':
            roundScore = playRoundYourStrategy(tableChancesFH, tableChancesSS, fhScoreObtained, ssScoreObtained)
        elif strategy == 'expected_value_strategy':
            roundScore = playRoundYourStrategyValue(tableChancesFH, tableChancesSS, fhScoreObtained, ssScoreObtained)
        else:
            raise ValueError("Unknown strategy")
        #print(f"Round {round_number} Score: {roundScore}")
        
        total_score += roundScore
        fhScoreObtained = True if roundScore == FULL_HOUSE_SCORE else fhScoreObtained
        ssScoreObtained = True if roundScore == SMALL_STRAIGHT_SCORE else ssScoreObtained
    
    return total_score

def runSimulations(num_simulations, tableChancesFH, tableChancesSS, strategy):
    total_scores = 0
    zero_hits = 0
    
    for _ in range(num_simulations):
        total_score = playGame(tableChancesFH, tableChancesSS, strategy)
        total_scores += total_score
        if total_score == 0:
            zero_hits += 1
    
    average_score = total_scores / num_simulations
    
    print(f"Strategy: {strategy}")
    print(f"Number of times score was 0: {zero_hits}")
    print(f"Average score over {num_simulations} simulations: {average_score}")
    
    return zero_hits, average_score

num_simulations = 1000000
tableChancesFH = readCSVFile('tableChanceForFH.csv')
tableChancesSS = readCSVFile('tableChanceForSS.csv')

print("Always the highest chance Strategy:")
zero_hits_your_strategy, average_score_your_strategy = runSimulations(num_simulations, tableChancesFH, tableChancesSS, 'highst_chance_strategy')

print("Expected Value Strategy:")
zero_hits_your_expcted_strategy, average_score_your_expected_strategy = runSimulations(num_simulations, tableChancesFH, tableChancesSS, 'expected_value_strategy')

print("\nAlways Roll All Dice Strategy:")
zero_hits_always_roll_all, average_score_always_roll_all = runSimulations(num_simulations, tableChancesFH, tableChancesSS, 'always_roll_all')

print("\nRandom First Roll Strategy:")
zero_hits_random_first_roll, average_score_random_first_roll = runSimulations(num_simulations, tableChancesFH, tableChancesSS, 'random_first_roll')