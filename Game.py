from tabnanny import check
from Pawns import initialStateOfPawns, movePawn, pawnsDict
from DrawBoard import DrawStart, DrawMove, DrawTable, ValidatePawnMove, DrawPawnMove
from Walls import placeWall, validWall, wallDict, numOfWalls, initialStateOfWalls, NumOfColoredWall
from Pathfinding import astar
from MinMax import minimax3, checkValue
import copy

saveDictWalls = {}
saveDictPawns = {}
saveDictTable = {}
tabla = list()


class Game:
    whoseTurnIs = True  # na potezu je X, posle svakog poteza menjati
    WhoPlayFirst = True  # prvi igra igrac/ false-racunar
    numOfTurns = 0
    n = 0
    m = 0
    brojZidova = 0
    initX1 = tuple()
    initX2 = tuple()
    initO1 = tuple()
    initO2 = tuple()

    def __init__(self, dimN, dimM, zidovi, X1: tuple, X2: tuple, O1: tuple, O2: tuple):
        self.n = dimN
        self.m = dimM
        self.brojZidova = zidovi
        self.initX1 = X1
        self.initX2 = X2
        self.initO1 = O1
        self.initO2 = O2

    def IsItGameOver(self):

        for x in pawnsDict['X']:
            if(x == self.initO1 or x == self.initO2):
                print("X won the game")
                return True

        for o in pawnsDict['O']:
            if(o == self.initX1 or o == self.initX2):
                print("O won the game")
                return True


# OVDE JE KRAJ KLASE ZA SAD
includePc = input("Da za pc, ne za 2igraca")
if(includePc == "da"):
    firstPlay = input(
        "Uneti True ukoliko prvo igra igrac, pritisnutu Enter ukoliko igra prvo PC: ")
n, m = [int(x) for x in input(
    "Unesite N x M dimenzije table, odvojiti razmakom: ").split()]

zidovi = int(input("Unesite broj zidova: "))
initxX1, inityX1 = [int(x) for x in input(
    "Unesite x i y koordinate od X1, odvojiti razmakom: ").split()]
initxX2, inityX2 = [int(x) for x in input(
    "Unesite x i y koordinate od X2, odvojiti razmakom: ").split()]
initxO1, inityO1 = [int(x) for x in input(
    "Unesite x i y koordinate od Y1, odvojiti razmakom: ").split()]
initxO2, inityO2 = [int(x) for x in input(
    "Unesite x i y koordinate od Y2, odvojiti razmakom: ").split()]


Game1 = Game(n, m, zidovi, (initxX1, inityX1),
             (initxX2, inityX2), (initxO1, inityO1), (initxO2, inityO2))

initialStateOfWalls(wallDict, zidovi)
initialStateOfPawns(pawnsDict, (initxX1, inityX1),
                    (initxX2, inityX2), (initxO1, inityO1), (initxO2, inityO2))
DrawStart(tabla, pawnsDict, Game1.n, Game1.m)

WrongParameters = False
if(includePc == "da"):
    while True:
        if Game1.whoseTurnIs == True:
            igrac1 = "X"
        else:
            igrac1 = "O"
        WrongParameters = False
        if(WrongParameters):
            print("Uneli ste nevazece parametre, molimo pokusajte ponovo! ")

        WrongParameters = True

        if((firstPlay != "True") and (Game1.numOfTurns == 0)):
            stanje = (tabla, pawnsDict, wallDict)
            minimax_return = minimax3(
                stanje, 2, False if firstPlay == "True" else True, n, m, (stanje, -1000), (stanje, 1000))
            tabla = copy.deepcopy(minimax_return[0][0])
            pawnsDict = copy.deepcopy(minimax_return[0][1])
            wallDict = copy.deepcopy(minimax_return[0][2])
            Game1.whoseTurnIs = not Game1.whoseTurnIs
            WrongParameters = False
            Game1.numOfTurns += 1
            DrawTable(tabla)
            continue

        if((firstPlay == "True" and igrac1 == "X") or (firstPlay != "True" and igrac1 == "O")):

            print("Trenutno je na potezu " + igrac1+": ")

            if(Game1.numOfTurns < zidovi*4):
                moveInput = input(
                    "Uneti zeljeni potez, primer [X 2] [6 3] [z 4 9]: ")
                koordinate = moveInput.split("] [")
                brojPesaka = int(koordinate[0][3])
                vrsta = int(koordinate[1].split(" ")[0])
                kolona = int(koordinate[1].split(" ")[1])
                bojaZida = koordinate[2].split(" ")[0]
                vrstaZid = int(koordinate[2].split(" ")[1])
                kln = koordinate[2].split(" ")[2]
                kolonaZid = int(kln.split("]")[0])

                if(NumOfColoredWall(wallDict, igrac1, bojaZida) == 0):
                    print("Nemate vise zidova zadate boje")
                    continue
            else:
                moveInput = input("Uneti zeljeni potez, primer [X 2] [6 3]: ")
                koordinate = moveInput.split("] [")
                brojPesaka = int(koordinate[0][3])
                vrsta = int(koordinate[1].split(" ")[0])
                kln = koordinate[1].split(" ")[1]
                kolona = int(kln.split("]")[0])
                bojaZida = 'p'

            spotAfterValidation = ValidatePawnMove(tabla,
                                                   pawnsDict, igrac1, brojPesaka, (vrsta, kolona))

            # Cuvanje starih vrednosti
            oldPawnsDict = copy.deepcopy(pawnsDict)
            oldWallDict = copy.deepcopy(wallDict)
            oldTable = copy.deepcopy(tabla)

            if(numOfWalls(wallDict, igrac1, bojaZida)):
                if (spotAfterValidation != False and validWall(wallDict, igrac1, bojaZida, (vrstaZid, kolonaZid), Game1.n, Game1.m)):

                    # Odigravanje poteza
                    DrawMove(tabla, pawnsDict, bojaZida, (vrstaZid, kolonaZid),
                             igrac1, brojPesaka, spotAfterValidation)
                    movePawn(pawnsDict, igrac1, brojPesaka,
                             spotAfterValidation)
                    placeWall(wallDict, igrac1, bojaZida,
                              (vrstaZid, kolonaZid))

                    # Provera da li postoji put do cilja, ako ne postoji vraca se na stare vrednosti i potez se racuna kao nevalidan (na potezu je isti igrac)
                    if((astar(tabla, pawnsDict['X'][0], pawnsDict['startO'][0]) and
                        astar(tabla, pawnsDict['X'][0], pawnsDict['startO'][1]) and
                        astar(tabla, pawnsDict['X'][1], pawnsDict['X'][0]) and
                        astar(tabla, pawnsDict['O'][0], pawnsDict['startX'][0]) and
                        astar(tabla, pawnsDict['O'][0], pawnsDict['startX'][1]) and
                            astar(tabla, pawnsDict['O'][1], pawnsDict['O'][0]))):
                        # Game1.whoseTurnIs = not Game1.whoseTurnIs
                        WrongParameters = False
                        Game1.numOfTurns += 1
                        DrawTable(tabla)
                        stanje = (tabla, pawnsDict, wallDict)
                        minimax_return = minimax3(
                            stanje, 2, False if firstPlay == "True" else True, n, m, (stanje, -1000), (stanje, 1000))
                        Game1.numOfTurns += 1
                        tabla = copy.deepcopy(minimax_return[0][0])
                        pawnsDict = copy.deepcopy(minimax_return[0][1])
                        wallDict = copy.deepcopy(minimax_return[0][2])
                        DrawTable(tabla)

                    else:
                        pawnsDict = copy.deepcopy(oldPawnsDict)
                        wallDict = copy.deepcopy(oldWallDict)
                        tabla = copy.deepcopy(oldTable)

            else:

                # Nije potrebno proveravati da li postoji put jer nema vise zidova za postavljanje
                if spotAfterValidation != False:

                    DrawPawnMove(tabla, pawnsDict, igrac1,
                                 brojPesaka, spotAfterValidation)
                    DrawTable(tabla)
                    movePawn(pawnsDict, igrac1, brojPesaka,
                             spotAfterValidation)

                    # Game1.whoseTurnIs = not Game1.whoseTurnIs
                    WrongParameters = False
                    Game1.numOfTurns += 1
                    stanje = (tabla, pawnsDict, wallDict)
                    minimax_return = minimax3(
                        stanje, 0, False if firstPlay == "True" else True, n, m, (stanje, -1000), (stanje, 1000))
                    Game1.numOfTurns += 1
                    tabla = copy.deepcopy(minimax_return[0][0])
                    pawnsDict = copy.deepcopy(minimax_return[0][1])
                    wallDict = copy.deepcopy(minimax_return[0][2])
                    DrawTable(tabla)

        if Game1.IsItGameOver():
            break
else:
    while True:
        if Game1.whoseTurnIs == True:
            igrac1 = "X"
        else:
            igrac1 = "O"
        WrongParameters = False
        if(WrongParameters):
            print("Uneli ste nevazece parametre, molimo pokusajte ponovo! ")

        WrongParameters = True

        print("Trenutno je na potezu " + igrac1+": ")

        if(Game1.numOfTurns < zidovi*4):
            moveInput = input(
                "Uneti zeljeni potez, primer [X 2] [6 3] [z 4 9]: ")
            koordinate = moveInput.split("] [")
            brojPesaka = int(koordinate[0][3])
            vrsta = int(koordinate[1].split(" ")[0])
            kolona = int(koordinate[1].split(" ")[1])
            bojaZida = koordinate[2].split(" ")[0]
            vrstaZid = int(koordinate[2].split(" ")[1])
            kln = koordinate[2].split(" ")[2]
            kolonaZid = int(kln.split("]")[0])

            if(NumOfColoredWall(wallDict, igrac1, bojaZida) == 0):
                print("Nemate vise zidova zadate boje")
                continue
        else:
            moveInput = input("Uneti zeljeni potez, primer [X 2] [6 3]: ")
            koordinate = moveInput.split("] [")
            brojPesaka = int(koordinate[0][3])
            vrsta = int(koordinate[1].split(" ")[0])
            kln = koordinate[1].split(" ")[1]
            kolona = int(kln.split("]")[0])
            bojaZida = 'p'

        spotAfterValidation = ValidatePawnMove(tabla,
                                               pawnsDict, igrac1, brojPesaka, (vrsta, kolona))

        # Cuvanje starih vrednosti
        oldPawnsDict = copy.deepcopy(pawnsDict)
        oldWallDict = copy.deepcopy(wallDict)
        oldTable = copy.deepcopy(tabla)

        if(numOfWalls(wallDict, igrac1, bojaZida)):
            if (spotAfterValidation != False and validWall(wallDict, igrac1, bojaZida, (vrstaZid, kolonaZid), Game1.n, Game1.m)):

                # Odigravanje poteza
                DrawMove(tabla, pawnsDict, bojaZida, (vrstaZid, kolonaZid),
                         igrac1, brojPesaka, spotAfterValidation)
                movePawn(pawnsDict, igrac1, brojPesaka, spotAfterValidation)
                placeWall(wallDict, igrac1, bojaZida, (vrstaZid, kolonaZid))
                temp = checkValue((tabla, pawnsDict, wallDict))

                # Provera da li postoji put do cilja, ako ne postoji vraca se na stare vrednosti i potez se racuna kao nevalidan (na potezu je isti igrac)
                if((astar(tabla, pawnsDict['X'][0], pawnsDict['startO'][0]) and
                    astar(tabla, pawnsDict['X'][0], pawnsDict['startO'][1]) and
                    astar(tabla, pawnsDict['X'][1], pawnsDict['X'][0]) and
                    astar(tabla, pawnsDict['O'][0], pawnsDict['startX'][0]) and
                    astar(tabla, pawnsDict['O'][0], pawnsDict['startX'][1]) and
                        astar(tabla, pawnsDict['O'][1], pawnsDict['O'][0]))):
                    Game1.whoseTurnIs = not Game1.whoseTurnIs
                    WrongParameters = False
                    Game1.numOfTurns += 1
                    DrawTable(tabla)

                else:
                    pawnsDict = copy.deepcopy(oldPawnsDict)
                    wallDict = copy.deepcopy(oldWallDict)
                    tabla = copy.deepcopy(oldTable)

        else:

            # Nije potrebno proveravati da li postoji put jer nema vise zidova za postavljanje
            if spotAfterValidation != False:
                DrawPawnMove(tabla, pawnsDict, igrac1,
                             brojPesaka, spotAfterValidation)
                DrawTable(tabla)
                movePawn(pawnsDict, igrac1, brojPesaka, spotAfterValidation)

                Game1.whoseTurnIs = not Game1.whoseTurnIs
                WrongParameters = False
                Game1.numOfTurns += 1

        if Game1.IsItGameOver():
            break
