# a honeycomb pattern simulator
# 21553103@student.uwa.edu.au
import numpy as np
import matplotlib.pyplot as plt
import random as rand

column = 64
row = 42

# directions
up = 0
left = 1
right = 2
down = 3

colors = dict()
colors[0] = 'black'
colors[1] = 'white'
colors[2] = 'red'
colors[3] = 'yellow'
direction = -1

'''
brood : 1
pollen : 2
honey : 3
sealedBrood : 4
'''
points = np.zeros((row, column), dtype=int)

weightCount = [0] * 9   # store the amount of different weight points
#pollenWeight = [0] * 9

emptyCell = 0
broodCell = -1
pollenCell = -2
honeyCell = -3

# define the function blocks
def refreshWeight(h, w):
    for i in range(h-1, h+2):
        if i > 0 and i < row:
            for j in range(w-1, w+2):
                if j > 0 and j < column:
                    if points[i, j] >= 0:
                        if points[i, j] > 0:
                            weightCount[points[i, j]] -= 1
                        points[i, j] += 1
                        weightCount[points[i, j]] += 1

def brood():
#    print "*****************brood******************"
    broodCells = np.where(points == broodCell)
    if len(broodCells[0]) == 0:
        broodRow = np.random.randint(row/2 - 10, row/2 - 5)
        broodColumn = np.random.randint(column/2 - 2, column/2 + 2)
        points[broodRow, broodColumn] = broodCell
        refreshWeight(broodRow, broodColumn)
        return broodRow, broodColumn
    else:
        curMaxWeight = 0
        weightList = []
        for i in range(1, len(weightCount)):
            if weightCount[i] > 0:
                weightList += [i]
        if len(weightList) > 2:
            weight = weightList[-1: -3: -1][np.random.randint(0, 2)]
        else:
            weight = weightList[-1] # change to weightList[0] will scatter brood cell into a stochastic way
        maxPosList = np.where(points == weight)     # find out the max weight location list
        index = np.random.randint(0, weightCount[weight]) # choose 1 location from max list
        posH = maxPosList[0][index]
        posW = maxPosList[1][index]
        points[posH, posW] = broodCell
        weightCount[weight] -= 1
        refreshWeight(posH, posW)
        return posH, posW

def refreshPollenWeight(h, w):
    for i in range(h-1, h+2):
        if i > 0 and i < row:
            for j in range(w-1, w+2):
                if j > 0 and j < column:
                    if points[i, j] >= 0:
                        if points[i, j] > 0:
                            weightCount[points[i, j]] -= 1
                        points[i, j] += 1
                        weightCount[points[i, j]] += 1

pollenChance = [0]*1 + [1]*3 + [2]*5
def pollen():
#    print "*****************pollen******************"
    # empty cells around brood cells which have weight >= 3
    emptyCellsNextBrood = np.where(points >= 3)
    tmp = np.transpose(np.asarray(emptyCellsNextBrood))
    emptyLen = len(emptyCellsNextBrood[0])
    choice = rand.choice(pollenChance)
    if emptyLen != 0:
        if choice == 0:
            t = tmp[:emptyLen/3]
        elif choice == 1:
            t = tmp[emptyLen/3:emptyLen*2/3]
        else:
            t = tmp[emptyLen*2/3:emptyLen]
        np.random.shuffle(t)
        if len(t[0]) != 0:
            points[t[0, 0], t[0, 1]] = pollenCell
            refreshPollenWeight(t[0, 0], t[0, 1])
            return t[0, 0], t[0, 1]

        avialibleCells = np.where(points == emptyCell)
        if len(avialibleCells[0]) != 0:
            return avialibleCells[0][0], avialibleCells[1][0]

def honey():
#    print "****************honey******************"
    # direction = np.random.randint(0, 2)
    emptyCells = np.where(points[row - 1] == emptyCell)
    if len(emptyCells[0]) != 0:
        np.random.shuffle(emptyCells[0])
        points[row - 1, emptyCells[0][0]] = honeyCell
        return row - 1, emptyCells[0][0]

    global direction
    direction *= -1
    for r in range(row - 2, -1, -1):
        emptyCells = np.where(points[r][::direction] == emptyCell)
        if len(emptyCells[0]) > 0:
            for col in emptyCells[0]:
                if r != row - 1:  # honey should be above pollen
                    # if len(np.where(points[:,col] == pollenCell)) == 0:
                    pollenInCol = False
                    for i in range(r, row):
                        if points[i, col] == pollenCell:
                            pollenInCol = True
                            break
                    if not pollenInCol:
                        points[r, col] = honeyCell
                        return r, col

    avialibleCells = np.where(points == emptyCell)
    if len(avialibleCells[0]) != 0:
        points[avialibleCells[0][0], avialibleCells[1][0]] = honeyCell
        return avialibleCells[0][0], avialibleCells[1][0]

def sealedBrood():
    pass

behaviors = {1 : brood,
             2 : pollen,
             3 : honey,
             4 : sealedBrood,
}
chance = [2]*1 + [3]*4
def choosePos(behaviorType):
    return behaviors[behaviorType]()

def behavior():
    return chance[np.random.randint(0, len(chance))]

minOviposition = 20
maxOviposition = 25

plt.axis([0, 64, 0, 64])
plt.ion()

t = 0
while True:
    t += 1
    broodCells = np.where(points == broodCell)
    if len(broodCells[0]) < row * column * 2/ 5:
        oviposition = np.random.randint(minOviposition, maxOviposition)
        for k in range(0, oviposition):
            i, j = choosePos(1)
            plt.scatter(j, i+j%2*0.5, s=50, c=colors[1], marker='H', edgecolors='black')
    else:
        break
    if t%50 == 0:
        plt.pause(1)

while True:
    t += 1
    behaviorType = behavior()
    if behaviorType == None:
        plt.pause(100)
    i, j = choosePos(behaviorType)
    plt.scatter(j, i+j%2*0.5, s=50, c=colors[behaviorType], marker='H', edgecolors='black')
    if t%150 == 0:
        plt.pause(0.01)
