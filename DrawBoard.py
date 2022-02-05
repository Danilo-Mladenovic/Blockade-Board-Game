from Pawns import pawnsDict, initialStateOfPawns
from Walls import wallDict

pozicije = list()


def DrawStart(tabla: list, pawnsPosition: dict, tableSizeN: int, tableSizeM: int):
    # Ovo se poziva samo za prvo iscrtavanje
    StartingBoardState(tableSizeN, tableSizeM)
    DrawPawns(pawnsPosition)
    StartingBoard(tabla, tableSizeN, tableSizeM)
    DrawWalls(tabla)
    DrawTable(tabla)


def DrawMove(tabla: list, pawnsPosition: dict, color: str, position: tuple, player: str, pawn: int, newSpot: tuple):
    # Ovo se poziva za svaki potez
    UpdatePawn(tabla, pawnsPosition, player, pawn, newSpot)
    AddWall(tabla, color, position)


def DrawPawnMove(tabla: list, pawnsPosition: dict, player: str, pawn: int, newSpot: tuple):
    # Ovo se poziva za svaki potez
    UpdatePawn(tabla, pawnsPosition, player, pawn, newSpot)


def StartingBoardState(tableSizeN: int, tableSizeM: int):
    # Pozicije je matrica sa pocetnim stanjima table - prazna mesta
    for i in range(0, tableSizeN):
        red = list()
        for j in range(0, tableSizeM):
            red.append(' ')
        pozicije.append(red)


def DrawPawns(pawnsPosition: dict):
    # Dodaju se igraci - ovo se poziva pri svakom pomeranju pesaka
    pozicije[pawnsPosition['X'][0][0] - 1][pawnsPosition['X'][0][1] - 1] = 'X'
    pozicije[pawnsPosition['X'][1][0] - 1][pawnsPosition['X'][1][1] - 1] = 'X'
    pozicije[pawnsPosition['O'][0][0] - 1][pawnsPosition['O'][0][1] - 1] = 'O'
    pozicije[pawnsPosition['O'][1][0] - 1][pawnsPosition['O'][1][1] - 1] = 'O'


def UpdatePawn(tabla: list, pawnsPosition: dict, player: str, pawn: int, newSpot: tuple):
    newX = newSpot[0] * 2 - 1
    newY = newSpot[1] * 2 - 1
    oldSpot = pawnsPosition[player][pawn - 1]

    oldX = oldSpot[0] * 2 - 1
    oldY = oldSpot[1] * 2 - 1

    if oldSpot in pawnsPosition["start" + player]:
        tabla[oldX][oldY] = "V" if player == "X" else "C"
        tabla[newX][newY] = player

        pozicije[oldSpot[0] - 1][oldSpot[1] -
                                 1] = "V" if player == "X" else "C"
        pozicije[newSpot[0] - 1][newSpot[1] - 1] = player
    else:
        # Brise se sa stare pozicije i unosi na novu
        # NE MENJA POZICIJE U PAWNS DICT!!!!
        tabla[oldX][oldY] = " "
        tabla[newX][newY] = player

        pozicije[oldSpot[0] - 1][oldSpot[1] - 1] = " "
        pozicije[newSpot[0] - 1][newSpot[1] - 1] = player


def ValidatePawnMove(tabla: list, pawnsPosition: dict, player: str, pawn: int, newSpot: tuple):

    # new_spot je nova pozicija u matrici sa zidovima, a newSpot je samo u matrici stanja
    newX = newSpot[0] * 2 - 1
    newY = newSpot[1] * 2 - 1
    # oldSpot je stara pozicija u matrici stanja
    oldSpot = pawnsPosition[player][pawn - 1]

    oldX = oldSpot[0] * 2 - 1
    oldY = oldSpot[1] * 2 - 1

    # Proverava da li je pomeranje ucinjeno za dva mesta ili za jedno mesto ka cilju
    goal = pawnsPosition['start' + ('O' if player == 'X' else 'X')]
    distance = abs(oldSpot[0]-newSpot[0])+abs(oldSpot[1]-newSpot[1])
    if(distance != 2):
        if(distance == 1 and goal[0] != newSpot and goal[1] != newSpot):
            return False
        elif(distance != 1):
            return False

    # Proverava da li je nova pozicija van granica table
    if (newX >= len(tabla) or newX < 0):
        return False
    elif (newY >= len(tabla[0]) or newY < 0):
        return False

    # Gore
    if(newSpot[0] < oldSpot[0] and newSpot[1] == oldSpot[1]):
        if(((tabla[newX+1][newY] == '===') if distance == 2 else False) or (tabla[newX+3][newY] == '===')):
            return False
        elif (((tabla[newX][newY] == "X") or (tabla[newX][newY] == "O")) and (tabla[newX+2][newY] == " ")):
            return (newSpot[0]+1, newSpot[1])
        else:
            return newSpot

    # Dole
    elif(newSpot[0] > oldSpot[0] and newSpot[1] == oldSpot[1]):
        if(((tabla[newX-1][newY] == '===') if distance == 2 else False) or (tabla[newX-3][newY] == '===')):
            return False
        elif (((tabla[newX][newY] == "X") or (tabla[newX][newY] == "O")) and (tabla[newX-2][newY] == " ")):
            return (newSpot[0]-1, newSpot[1])
        else:
            return newSpot

    # Levo
    elif(newSpot[0] == oldSpot[0] and newSpot[1] < oldSpot[1]):
        if(((tabla[newX][newY+1] == ' ||') if distance == 2 else False) or (tabla[newX][newY+3] == ' ||')):
            return False
        elif (((tabla[newX][newY] == "X") or (tabla[newX][newY] == "O")) and (tabla[newX][newY+2] == " ")):
            return (newSpot[0], newSpot[1]+1)
        else:
            return newSpot

    # Desno
    elif(newSpot[0] == oldSpot[0] and newSpot[1] > oldSpot[1]):
        if(((tabla[newX][newY-1] == ' ||') if distance == 2 else False) or (tabla[newX][newY-3] == ' ||')):
            return False
        elif (((tabla[newX][newY] == "X") or (tabla[newX][newY] == "O")) and (tabla[newX][newY-2] == " ")):
            return (newSpot[0], newSpot[1]-1)
        else:
            return newSpot

    # Zauzete dijagonale
    elif (tabla[newX][newY] != " "):
        return False

    # Dijagonala gore levo
    elif newSpot[0] == oldSpot[0] - 1 and newSpot[1] == oldSpot[1] - 1:
        if ((tabla[newX][newY + 1] == ' ||' and tabla[newX + 2][newY + 1] == ' ||') or
            (tabla[newX + 1][newY] == '===' and tabla[newX + 1][newY + 2] == '===') or
            (tabla[newX][newY + 1] == ' ||' and tabla[newX + 1][newY] == '===') or
                (tabla[newX + 2][newY + 1] == ' ||' and tabla[newX + 1][newY + 2] == '===')):
            return False
    # Dijagonala gore desno
    elif newSpot[0] == oldSpot[0] - 1 and newSpot[1] == oldSpot[1] + 1:
        if ((tabla[newX][newY - 1] == ' ||' and tabla[newX + 2][newY - 1] == ' ||') or
            (tabla[newX + 1][newY] == '===' and tabla[newX + 1][newY - 2] == '===') or
            (tabla[newX][newY - 1] == ' ||' and tabla[newX + 1][newY] == '===') or
                (tabla[newX + 2][newY - 1] == ' ||' and tabla[newX + 1][newY - 2] == '===')):
            return False
    # Dijagonala dole desno
    elif newSpot[0] == oldSpot[0] + 1 and newSpot[1] == oldSpot[1] + 1:
        if ((tabla[newX - 2][newY - 1] == ' ||' and tabla[newX][newY - 1] == ' ||') or
            (tabla[newX - 1][newY - 2] == '===' and tabla[newX - 1][newY] == '===') or
            (tabla[newX][newY - 1] == ' ||' and tabla[newX - 1][newY] == '===') or
                (tabla[newX - 2][newY - 1] == ' ||' and tabla[newX - 1][newY - 2] == '===')):
            return False
    # Dijagonala dole levo
    elif newSpot[0] == oldSpot[0] + 1 and newSpot[1] == oldSpot[1] - 1:
        if ((tabla[newX - 2][newY + 1] == ' ||' and tabla[newX][newY + 1] == ' ||') or
            (tabla[newX - 1][newY] == '===' and tabla[newX - 1][newY + 2] == '===') or
            (tabla[newX][newY + 1] == ' ||' and tabla[newX - 1][newY] == '===') or
                (tabla[newX - 2][newY + 1] == ' ||' and tabla[newX - 1][newY + 2] == '===')):
            return False

    return newSpot


def StartingBoard(tabla: list, tableSizeN: int, tableSizeM: int):
    # Tabla je matrica koja ce da se stampa, sadrzi igrace, prazna polja i zidove
    newTableSizeN = tableSizeN * 2 + 1
    newTableSizeM = tableSizeM * 2 + 1
    for i in range(0, newTableSizeN):
        red = list()
        if (i % 2 == 0):
            for j in range(0, newTableSizeM):
                if (i == 0 or i == newTableSizeN - 1):
                    red.append(" " if (j % 2 == 0) else "===")
                else:
                    red.append(" " if (j % 2 == 0) else "———")
        else:
            for j in range(0, newTableSizeM):
                red.append(" | " if (j % 2 == 0)
                           else pozicije[(i - 1) // 2][(j - 1) // 2])
            red[0] = "||"
            red[newTableSizeM - 1] = "||"
        tabla.append(red)


def DrawWalls(tabla: list):
    # Dodavanje zidova u tablu koja se iscrtava
    for i in range(0, len(list(wallDict['H']))):
        tabla[(wallDict['H'][i][0] + 1) *
              2][wallDict['H'][i][1] * 2 + 1] = "==="
        tabla[(wallDict['H'][i][0] + 1) *
              2][wallDict['H'][i][1] * 2 + 3] = "==="

    for i in range(0, len(list(wallDict['V']))):
        tabla[wallDict['V'][i][0] * 2 +
              1][(wallDict['V'][i][1] + 1) * 2] = " ||"
        tabla[wallDict['V'][i][0] * 2 +
              3][(wallDict['V'][i][1] + 1) * 2] = " ||"


def AddWall(tabla: list, color: str, position: tuple):
    if color == 'p':
        tabla[position[0] * 2][position[1] * 2 - 1] = "==="
        tabla[position[0] * 2][position[1] * 2 + 1] = "==="
    else:
        tabla[position[0] * 2 - 1][position[1] * 2] = " ||"
        tabla[position[0] * 2 + 1][position[1] * 2] = " ||"


def DrawTable(tabla: list):

    # Pomocna matrica koja ce da sadrzi i indekse
    itabla = list()
    indeksi = list()
    indeksi.append(" ")
    for i in range(0, len(tabla[0])):
        hex_index = hex((i + 1) // 2).split('x')[-1]
        indeksi.append((" " + hex_index + (" " if len(hex_index)
                       == 1 else "")) if (i % 2 != 0) else " ")
    itabla.append(indeksi)

    for i in range(0, len(tabla)):
        ired = list()
        ired.append((hex((i + 1) // 2).split('x')
                    [-1]) if (i % 2 != 0) else " ")
        for j in range(0, len(tabla[i])):
            ired.append(tabla[i][j])
        ired.append((hex((i + 1) // 2).split('x')
                    [-1]) if (i % 2 != 0) else " ")
        itabla.append(ired)
    itabla.append(indeksi)

    # Iscrtava matricu table, treba da se pozove nakon svakog dodavanja zida (AddWalls)
    for i in range(0, len(itabla)):
        for j in range(0, len(itabla[i])):
            print(itabla[i][j], end=" ")
        print('\n')
