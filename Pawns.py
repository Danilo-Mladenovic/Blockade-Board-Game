pawnsDict = {
    'X': [],
    'O': [],
    'startX': [],
    'startO': []
}


def initialStateOfPawns(dictionary: dict, X1: tuple, X2: tuple, O1: tuple, O2: tuple):
    dictionary['X'] = [X1, X2]
    dictionary['startX'] = [X1, X2]
    dictionary['O'] = [O1, O2]
    dictionary['startO'] = [O1, O2]


def movePawn(dictionary: dict, player: str, pawn: int, newSpot: tuple):
    dictionary['X' if player == 'X' else 'O'][0 if pawn == 1 else 1] = newSpot
