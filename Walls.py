wallDict = {
    'V': [],
    'H': [],
    'numX': [],
    'numO': []
}


def initialStateOfWalls(dictionary: dict, k: int):
    dictionary['numX'] = [k, k]
    dictionary['numO'] = [k, k]


def placeWall(dictionary: dict, player: str, color: str, newSpot: tuple):
    dictionary['V' if color == 'z' else 'H'].append(newSpot)
    dictionary['numX' if player ==
               'X' else 'numO'][0 if color == 'z' else 1] -= 1


def NumOfColoredWall(dictionary: dict, player: str, color: str):
    return dictionary['num'+player][0 if color == 'z' else 1]


def numOfWalls(wallDict: dict, player: str, color: str):
    if color == "p":
        if wallDict["num" + player][1] == 0:
            return False
    elif color == "z":
        if wallDict["num" + player][0] == 0:
            return False
    return True


def validWall(wallDict: dict, player: str, color: str, newsSpot: tuple, tableSizeN, tableSizeM):
    if color == "p":
        if wallDict["num" + player][1] == 0:
            return False
    elif color == "z":
        if wallDict["num" + player][0] == 0:
            return False

    if (newsSpot[0] > tableSizeN-1) or (newsSpot[1] > tableSizeM-1):
        return False
    if(color == 'z'):
        for x in wallDict['V']:
            if ((x == newsSpot) or
                (x[1] == newsSpot[1] and x[0] == newsSpot[0]+1) or
                    (x[1] == newsSpot[1] and x[0] == newsSpot[0] - 1)):
                return False
        for x in wallDict['H']:
            if(newsSpot[0] == x[0] and newsSpot[1] == x[1]):
                return False
        return True
    if(color == 'p'):
        for x in wallDict['H']:
            if ((x == newsSpot) or
                (x[0] == newsSpot[0] and x[1] == newsSpot[1]+1) or
                    (x[0] == newsSpot[0] and x[1] == newsSpot[1]-1)):
                return False
        for x in wallDict['V']:
            if(newsSpot[0] == x[0] and newsSpot[1] == x[1]):
                return False
        return True
