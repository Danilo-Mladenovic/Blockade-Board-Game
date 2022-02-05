from Pawns import movePawn
from DrawBoard import DrawMove, ValidatePawnMove, DrawPawnMove
from Walls import placeWall, validWall, numOfWalls
from Pathfinding import astar
import copy


def changeState(tabla: list, pawnsPositions: dict, color: str, position: tuple, player: str, pawn: int, newSpot: tuple, wall: bool):
    tableForSimulation = copy.deepcopy(tabla)
    if(wall):
        DrawMove(tableForSimulation, pawnsPositions, color, position,
                 player, pawn, newSpot)
    else:
        DrawPawnMove(tableForSimulation, pawnsPositions, player,
                     pawn, newSpot)
    return tableForSimulation


def addEndGoalsToList(spots: list, coord: tuple, end1: tuple, end2: tuple):
    if(abs(coord[0]-end1[0])+abs(coord[1]-end1[1]) == 1):
        spots.append(end1)
    if(abs(coord[0]-end2[0])+abs(coord[1]-end2[1]) == 1):
        spots.append(end2)


def allValidStates(tabla: list, pawnsDict: dict, wallDict: dict, player: str, pawn: int, tableSizeN: int, tableSizeM: int):
    valid = list()
    validSpots = list()
    coord: tuple = pawnsDict[player][pawn-1]
    endForX1 = pawnsDict['startO'][0]
    endForX2 = pawnsDict['startO'][1]
    endForO1 = pawnsDict['startX'][0]
    endForO2 = pawnsDict['startX'][1]

    if pawnsDict['startX'][0][0] < pawnsDict['startO'][0][0]:
        # startna pozicija X je visa od O
        if player == 'X':
            spotsToCheck: list = [(coord[0]+2, coord[1]), (coord[0], coord[1]+2), (coord[0], coord[1]-2),
                                  (coord[0]+1, coord[1]+1), (coord[0]+1, coord[1]-1)]
            addEndGoalsToList(spotsToCheck, coord, endForX1, endForX2)
        else:
            spotsToCheck: list = [(coord[0]-2, coord[1]), (coord[0], coord[1]+2), (coord[0], coord[1]-2),
                                  (coord[0]-1, coord[1]+1), (coord[0]-1, coord[1]-1)]
            addEndGoalsToList(spotsToCheck, coord, endForO1, endForO2)
    else:
        # Startna pozicija X je niza od O
        if player == 'X':
            spotsToCheck: list = [(coord[0]-2, coord[1]), (coord[0], coord[1]+2), (coord[0], coord[1]-2),
                                  (coord[0]-1, coord[1]+1), (coord[0]-1, coord[1]-1)]
            addEndGoalsToList(spotsToCheck, coord, endForX1, endForX2)
        else:
            spotsToCheck: list = [(coord[0]+2, coord[1]), (coord[0], coord[1]+2), (coord[0], coord[1]-2),
                                  (coord[0]+1, coord[1]+1), (coord[0]+1, coord[1]-1)]
            addEndGoalsToList(spotsToCheck, coord, endForO1, endForO2)

    for s in spotsToCheck:
        spotAfterValidation = ValidatePawnMove(tabla,
                                               pawnsDict, player, pawn, s)
        if(spotAfterValidation):
            validSpots.append(spotAfterValidation)

    oldPawnsDict = copy.deepcopy(pawnsDict)
    oldWallDict = copy.deepcopy(wallDict)

    boje = ["p", "z"]
    for i in range(0, 2):
        bojaZida = boje[i]
        if(numOfWalls(wallDict, player, bojaZida)):
            for v in validSpots:
                for i in range(1, tableSizeN, 2):
                    for j in range(1, tableSizeM, 2):
                        if (validWall(oldWallDict, player, bojaZida, (i, j), tableSizeN, tableSizeM)):
                            newTable = changeState(tabla, oldPawnsDict, bojaZida,
                                                   (i, j), player, pawn, v, True)
                            movePawn(oldPawnsDict, player, pawn,
                                     v)
                            placeWall(oldWallDict, player, bojaZida, (i, j))

                            if((astar(newTable, oldPawnsDict['X'][0], oldPawnsDict['startO'][0]) and
                                astar(newTable, oldPawnsDict['X'][0], oldPawnsDict['startO'][1]) and
                                astar(newTable, oldPawnsDict['X'][1], oldPawnsDict['X'][0]) and
                                astar(newTable, oldPawnsDict['O'][0], oldPawnsDict['startX'][0]) and
                                astar(newTable, oldPawnsDict['O'][0], oldPawnsDict['startX'][1]) and
                                    astar(newTable, oldPawnsDict['O'][1], oldPawnsDict['O'][0]))):
                                valid.append(
                                    (newTable, oldPawnsDict, oldWallDict))

                            oldPawnsDict = copy.deepcopy(pawnsDict)
                            oldWallDict = copy.deepcopy(wallDict)
        else:
            for v in validSpots:
                newTable = changeState(tabla, oldPawnsDict, "",
                                       (0, 0), player, pawn, v, False)
                movePawn(oldPawnsDict, player, pawn,
                         v)
                valid.append((newTable, oldPawnsDict, oldWallDict))
                oldPawnsDict = copy.deepcopy(pawnsDict)
    return valid
