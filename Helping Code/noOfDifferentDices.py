# noDices = 5
# diceValues = range(1,7)
# outcomes = []
# uniqueOutcomes = []

# for dice1 in diceValues:
#     for dice2 in diceValues:
#         for dice3 in diceValues:
#             for dice4 in diceValues:
#                 for dice5 in diceValues:
#                     outcome = [dice1, dice2, dice3, dice4, dice5]
#                     outcome.sort()
#                     outcomes.append(outcome)


# outcomes.sort()

# for i in range(len(outcomes) - 1):
#     if outcomes[i] != outcomes[i + 1]:
#         uniqueOutcomes.append(outcomes[i])

# uniqueOutcomes.append(outcomes[-1])  


#print(uniqueOutcomes)
#print(len(uniqueOutcomes))


def checkThreeOfAKind(combination):
    freqVector = [0] * 6
    for die in combination:
        freqVector[die - 1] += 1
    for no in freqVector:
        if no >= 3:
            return True
    return False

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


def rolls(n, k=6):
    if n:
        for i in range(k, 0, -1):
            for roll in rolls(n-1, i):
                yield roll + [i]
    else:
        yield []

distinct_rolls = list(rolls(5)) 

def generateAllRolls(n, k=6):
    if n == 0:
        yield []
    else:
        for i in range(1, k+1):
            for roll in generateAllRolls(n-1, k):
                yield [i] + roll

all_rolls = list(generateAllRolls(5))
print(len(all_rolls))

no = 0
for roll in all_rolls:
    if checkLargeStraight(roll):
        no += 1
#         print(roll)
#         print("        ")

# print("----------------",no, "------------------")

scoreboard = {
    "Ones": -1,
    "Twos": -1,
    "Threes": -1,
    "Fours": -1,
    "Fives": -1,
    "Sixes": -1,
    "ToaK": -1,
    "FoaK": -1,
    "FH": -1,
    "SS": -1,
    "LS": -1,
    "Yathzee": -1,
    "chance" : -1
}

# file = "CSV_Tables/Table"
# for key in scoreboard.keys():
#     if scoreboard[key] == -1:
#         filename = file + key + ".csv"
#         tableChances = read
        
