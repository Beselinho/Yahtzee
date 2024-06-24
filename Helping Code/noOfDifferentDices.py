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


def rolls(n, k=6):
    if n:
        for i in range(k, 0, -1):
            for roll in rolls(n-1, i):
                yield roll + [i]
    else:
        yield []

distinct_rolls = list(rolls(5)) 

for roll in distinct_rolls:
    print(roll)
    print("        ")
