import pygame
from pygame.locals import *
import random as rd


#scores
ONES_SCORE = 4.4
TWOS_SCORE = 9.15
THREES_SCORE = 13.9
FOURS_SCORE = 18.65
FIVES_SCORE = 23.05
SIXES_SCORE = 27.8
AVERAGE_THREE_OF_A_KIND_SCORE = 18
AVERAGE_FOUR_OF_A_KIND_SCORE = 18
FULL_HOUSE_SCORE = 25
SMALL_STRAIGHT_SCORE = 30
LARGE_STRAIGHT_SCORE = 40
YATHZEE_SCORE = 50

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
HEADER_HEIGHT = 50
ROW_HEIGHT = SCREEN_HEIGHT / 15
COLUMN_WIDTH = SCREEN_WIDTH // 2

#Images
imagePath = "interfaceMedia/dice"

# Colours
blackColour = (0, 0, 0)
whiteColour = (255, 255, 255)
greyColour = (211, 211, 211)
buttonColour = (0, 200, 0)
buttonHoverColour = (0, 250, 0)

#Distances
lastQuarter = 3 * SCREEN_WIDTH // 4
lastQuarterHalf = 3.5 * SCREEN_WIDTH // 4
heightFirstQuarter = SCREEN_HEIGHT // 4
heightThirdQuarter = 3 * SCREEN_HEIGHT // 4
heightSecondQuarter = 2 * SCREEN_HEIGHT // 4
widthHalfQuarter = SCREEN_WIDTH // 8 
xPadding = 10
yPadding = 15
scorePadding = 70


#buttonRelated
buttonWidth = 200
buttonHeight = 50
xButton = SCREEN_WIDTH // 4 + 75    
yButton = heightThirdQuarter - buttonHeight - 20
buttonRect = pygame.Rect(xButton, yButton, buttonWidth, buttonHeight)
buttonText = "Roll"

#diceRelated
scaledWidthOnBoard = 125
scaledHeightOnBoard = 125
sclaedWidthKept = 90
scaledHeightKept = 90
distanceBetweenDice = 40
diceCombination = [1,2,3,4,5]


#positions
# table_positions = [{'x': 70 + i * (scaledWidthOnBoard + distanceBetweenDice), 'y': heightFirstQuarter, 'occupied': False} for i in range(5)]
# kept_positions = [{'x': widthHalfQuarter + 10 + i * (scaledWidthOnBoard // 2 + 10), 'y': heightThirdQuarter + 10, 'occupied': False} for i in range(5)]
# dice_positions = [{'original': (70 + i * (scaledWidthOnBoard + distanceBetweenDice), heightFirstQuarter), 'current': 'original'} for i in range(len(diceCombination))]
table_positions = [
    {'value': 1, 'position': (50, 100)},
    {'value': 2, 'position': (150, 100)},
    {'value': 3, 'position': (250, 100)},
    {'value': 4, 'position': (350, 100)},
    {'value': 5, 'position': (450, 100)}
]

kept_positions = [
    {'value': -1, 'position': (50, 300)},
    {'value': -1, 'position': (150, 300)},
    {'value': -1, 'position': (250, 300)},
    {'value': -1, 'position': (350, 300)},
    {'value': -1, 'position': (450, 300)}
]


#tablePositionsArray = 


#diceVectors
table_dice = []
kept_dice = []

#fonts
font = pygame.font.SysFont(None, 30)
biggerFont = pygame.font.SysFont(None, 50)
titleFont = pygame.font.SysFont(None, 70)

#roundAndRoll
round = 1
roll = 0
max_rolls = 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
selectedBox = -1
scoreboard = [0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]


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
    largeSequence1 = [1, 2, 3, 4, 5]
    largeSequence2 = [2, 3, 4, 5, 6]
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

def rollDice(num_dice):
    return [rd.randint(1, 6) for _ in range(num_dice)]

def drawKeepSquare(round):
    pygame.draw.line(screen, blackColour, (widthHalfQuarter, heightThirdQuarter), (widthHalfQuarter, SCREEN_HEIGHT), width=5)
    pygame.draw.line(screen, blackColour, (0, heightThirdQuarter), (lastQuarter, heightThirdQuarter), width=5)
    drawText('Round', font, blackColour, screen, 35, heightThirdQuarter + 10)
    drawText(str(round), biggerFont, blackColour, screen, 35, heightThirdQuarter + 60)
    drawText('/13', biggerFont, blackColour, screen, 55, heightThirdQuarter + 60)

def loadDiceImages():
    for dice in table_positions + kept_positions:
        if dice['value'] == -1:
            continue  # Skip empty slots
        
        dice_image = str(dice['value']) + ".png"
        image = pygame.image.load(imagePath + dice_image)
        
        if dice in kept_positions:
            image = pygame.transform.scale(image, (scaledWidthOnBoard // 2, scaledHeightOnBoard // 2))
        else:
            image = pygame.transform.scale(image, (scaledWidthOnBoard, scaledHeightOnBoard))
        
        x, y = dice['position']
        screen.blit(image, (x, y))
        

def toggleDicePosition(mouse_pos):
    def move_dice(source, target):
        # Find first empty spot in target
        for slot in target:
            if slot['value'] == -1:
                slot['value'] = dice['value']
                dice['value'] = -1
                break
        # Reorganize the source to remove gaps
        source[:] = [slot for slot in source if slot['value'] != -1] + \
                    [{'value': -1, 'position': slot['position']} for slot in source if slot['value'] == -1]

    for dice in table_positions:
        if dice['value'] == -1:
            continue
        x, y = dice['position']
        image_rect = pygame.Rect(x, y, scaledWidthOnBoard, scaledHeightOnBoard)
        if image_rect.collidepoint(mouse_pos):
            move_dice(table_positions, kept_positions)
            return

    for dice in kept_positions:
        if dice['value'] == -1:
            continue
        x, y = dice['position']
        image_rect = pygame.Rect(x, y, scaledWidthOnBoard // 2, scaledHeightOnBoard // 2)
        if image_rect.collidepoint(mouse_pos):
            move_dice(kept_positions, table_positions)
            return


def drawText(text, font, color, surface, x, y):
    textObj = font.render(text, True, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)

def drawButton(surface, rect, text, font, color, hoverColor):
    mousePos = pygame.mouse.get_pos()
    if rect.collidepoint(mousePos):
        pygame.draw.rect(surface, hoverColor, rect)
        if pygame.mouse.get_pressed()[0]:  # If the left mouse button is pressed
            global diceCombination
            diceCombination = rollDice(5)
    else:
        pygame.draw.rect(surface, color, rect)
    
    textSurface = font.render(text, True, blackColour)
    textRect = textSurface.get_rect(center=rect.center)
    surface.blit(textSurface, textRect)


def drawTitle():
    drawText('Yahtzee', titleFont, blackColour, screen, SCREEN_WIDTH // 4, heightFirstQuarter / 10)

def drawTable(diceCombination):
    global selectedBox
    global scoreboard

    drawText('Combination', font, blackColour, screen, lastQuarter + 20, yPadding)
    drawText('Score', font, blackColour, screen, lastQuarterHalf + 40, yPadding)

    for i in range(15):
        yCoord = HEADER_HEIGHT + i * ROW_HEIGHT 
        pygame.draw.line(screen, blackColour, (lastQuarter, yCoord), (SCREEN_WIDTH, yCoord))

        if i == 0:
            drawText('Aces', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            localScore = sum(dice for dice in diceCombination if dice == 1)
            if localScore != 0 and scoreboard[i + 1] == -1:
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 1:
            drawText('Twos', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            localScore = sum(dice for dice in diceCombination if dice == 2)
            if localScore != 0 and scoreboard[i + 1] == -1:
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 2:
            drawText('Threes', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            localScore = sum(dice for dice in diceCombination if dice == 3)
            if localScore != 0 and scoreboard[i + 1] == -1:
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 3:
            drawText('Fours', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            localScore = sum(dice for dice in diceCombination if dice == 4)
            if localScore != 0 and scoreboard[i + 1] == -1:
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 4:
            drawText('Fives', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            localScore = sum(dice for dice in diceCombination if dice == 5)
            if localScore != 0 and scoreboard[i + 1] == -1:
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 5:
            drawText('Sixes', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            localScore = sum(dice for dice in diceCombination if dice == 6)
            if localScore != 0 and scoreboard[i + 1] == -1:
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 6:
            drawText('Bonus', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
        elif i == 7:
            drawText('Three of a kind', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            if checkThreeOfAKind(diceCombination) and scoreboard[i] == -1:
                localScore = sum(diceCombination)
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 8:
            drawText('Four of a kind', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            if checkFourOfAKind(diceCombination) and scoreboard[i] == -1:
                localScore = sum(diceCombination)
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 9:
            drawText('Full House', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            if checkFullHouse(diceCombination) and scoreboard[i] == -1:
                localScore = 25
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 10:
            drawText('Small Straight', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            if checkSmallStraight(diceCombination) and scoreboard[i] == -1:
                localScore = 30
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 11:
            drawText('Large Straight', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            if checkLargeStraight(diceCombination) and scoreboard[i] == -1:
                localScore = 40
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 12:
            drawText('Yahtzee', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            if checkYathzee(diceCombination) and scoreboard[i] == -1:
                localScore = 50
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)
        elif i == 13:
            drawText('Chance', font, blackColour, screen, lastQuarter + xPadding, yCoord + yPadding)
            localScore = sum(diceCombination)
            if scoreboard[i] == -1:
                drawText(str(localScore), font, greyColour if i != selectedBox else blackColour, screen, lastQuarterHalf + scorePadding, yCoord + yPadding)

    pygame.draw.line(screen, blackColour, (lastQuarter, 0), (SCREEN_WIDTH, 0), width=5)
    pygame.draw.line(screen, blackColour, (lastQuarter, 0), (lastQuarter, SCREEN_HEIGHT), width=5)
    pygame.draw.line(screen, blackColour, (lastQuarterHalf, 0), (lastQuarterHalf, SCREEN_HEIGHT))
    pygame.draw.line(screen, blackColour, (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), width=5)

# Main loop
round = 1
run = True
while run:
    screen.fill(whiteColour)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            toggleDicePosition(pygame.mouse.get_pos())
    
    drawTitle()
    drawButton(screen, buttonRect, buttonText, font, buttonColour, buttonHoverColour)
    drawTable(diceCombination)
    drawKeepSquare(round)
    loadDiceImages()
    
    pygame.display.update()

pygame.quit()
