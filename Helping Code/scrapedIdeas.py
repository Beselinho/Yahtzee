# def expectiMax4Kept(combination):
#     maximumScore = 0
#     positionOfDiceRolled = []
#     ok = 1
#     expectiMaxScores = [0] * 6
#     startingScore = checkScore(combination)
#     for rolledDice in range(5): 
#         outcome = []
#         #CP = Combination Possible
#         allCP = []
#         uniqueCP = []
#         #savedDice = combination
#         for dice1 in diceValues:
#             outcome = combination.copy()
#             outcome[rolledDice] = dice1
#             outcome.sort()
#             allCP.append(outcome)
                        
#         allCP.sort()
#         for i in range(len(allCP) - 1):
#             if allCP[i] != allCP[i + 1]:
#                 uniqueCP.append(allCP[i])
#         uniqueCP.append(allCP[-1])
        
    
#         childScore = 0
#         for finalCombination in uniqueCP:
#             score = checkScore(finalCombination)
#             childScore += score
        
#         childScore = childScore / len(uniqueCP)
#         expectiMaxScores[rolledDice + 1] = childScore
#     print(expectiMaxScores)
    
    
#     for dice, score in enumerate(expectiMaxScores):
#         if score > maximumScore:
#             maximumScore = score
#             positionOfDiceRolled = dice
#     if startingScore > maximumScore:
#         maximumScore = startingScore
#         ok = 0
            
#     print("Expecti Max Score chosen :\n", maximumScore)
#     if ok:
#         print("Postion of dice to be rolled chosen:\n", positionOfDiceRolled)
#     else:
#         print("All dice were kept")


# # def expectiMax1(combination):
# #     maximumScore = 0
# #     positionOfDiceKept = -1
# #     ok = 1
# #     expectiMaxScores = [0] * 6
# #     startingScore = checkScore(combination)
# #     for keptDice in range(5): 
# #         outcome = []
# #         #CP = Combination Possible
# #         allCP = []
# #         uniqueCP = []
        
# #         savedDice = combination[keptDice]
# #         for dice1 in diceValues:
# #             for dice2 in diceValues:
# #                 for dice3 in diceValues:
# #                     for dice4 in diceValues:
# #                         outcome = [dice1, dice2, dice3, dice4, savedDice]
# #                         outcome.sort()
# #                         allCP.append(outcome)
                        
# #         allCP.sort()
# #         for i in range(len(allCP) - 1):
# #             if allCP[i] != allCP[i + 1]:
# #                 uniqueCP.append(allCP[i])
# #         uniqueCP.append(allCP[-1])
    
# #         childScore = 0
# #         for finalCombination in uniqueCP:
# #             score = checkScore(finalCombination)
# #             childScore += score
        
# #         childScore = childScore / len(uniqueCP)
# #         expectiMaxScores[keptDice + 1] = childScore
# #         print(expectiMaxScores)
    
    
# #     for dice, score in enumerate(expectiMaxScores):
# #         if score > maximumScore:
# #             maximumScore = score
# #             positionOfDiceKept = dice
# #     if startingScore > maximumScore:
# #         maximumScore = startingScore
# #         ok = 0
            
# #     print("Expecti Max Score chosen :\n", maximumScore)
# #     if ok:
# #         print("Postion of dice to be kept chosen:\n", positionOfDiceKept)
# #     else:
# #         print("All dice were kept")

# def expectiMaxYield(combination):
#     startingScore = checkScore(combination)
#     expectiMaxScores = [0] * 6
#     maximumScore = 0
#     positionOfDiceKept = -1
#     numberOfDicesKept = 4 
#     diceWereRolled = 1
    
#     for keptDice in range(5): 
#         outcome = []
#         savedDice = combination[keptDice]
        
#         outcome = list(generateRolls(numberOfDicesKept))               
#         totalScore = 0
#         for finalCombination in outcome:
#             finalCombination.append(savedDice)
#             score = checkScore(finalCombination)
#             totalScore += score
        
#         totalScore = totalScore / len(outcome)
#         expectiMaxScores[keptDice + 1] = totalScore
#     print(expectiMaxScores)
    
    
#     for dice, score in enumerate(expectiMaxScores):
#         if score > maximumScore:
#             maximumScore = score
#             positionOfDiceKept = dice
#     if startingScore > maximumScore:
#         maximumScore = startingScore
#         diceWereRolled = 0
            
#     print("Expecti Max Score chosen :\n", maximumScore)
#     if diceWereRolled:
#         print("Postion of dice to be kept chosen:\n", positionOfDiceKept)
#     else:
#         print("All dice were kept")        
# def expectiMaxTwoKept(combination):
#     startingScore = checkScore(combination)
#     expectiMaxScores = [[0] * 6 for _ in range(6)]
#     maximumScore = 0
#     positionOfDiceKept = []
#     noOfDiceKept = 2 
#     diceWereRolled = 1
#     for keptDice1, keptDice2  in allPossible2DiceKept: 
#         savedDice = []
#         outcome = []
#         savedDice.append(combination[keptDice1])
#         savedDice.append(combination[keptDice2])
#         print(savedDice)
        
#         outcome = list(generateRolls(numberOfDices - noOfDiceKept))               
#         totalScore = 0
#         for finalCombination in outcome:
#             finalCombination.append(savedDice[0])
#             finalCombination.append(savedDice[1])
#             score = checkScore(finalCombination)
#             totalScore += score
        
#         totalScore = totalScore / len(outcome)
#         expectiMaxScores[keptDice1 + 1][keptDice2 + 1] = totalScore
#     print(expectiMaxScores)
    
#     for i in range(len(expectiMaxScores)):
#         for j in range(len(expectiMaxScores)):
#             if expectiMaxScores[i][j] > maximumScore:
#                 maximumScore = expectiMaxScores[i][j]
#                 positionOfDiceKept = [i, j]
                
#     if startingScore > maximumScore:
#         maximumScore = startingScore
#         diceWereRolled = 0
            
#     print("Expecti Max Score chosen :\n", maximumScore)
#     if diceWereRolled:
#         print("Postion of dice to be kept chosen:\n", positionOfDiceKept)
#     else:
#         print("All dice were kept")     



#print(expectiMax4Kept([1,2,6,5,3]))
#print(expectiMaxYield([1,2,5,3,3]))
#print(expectiMaxTwoKept([1,2,5,5,3]))
                  
