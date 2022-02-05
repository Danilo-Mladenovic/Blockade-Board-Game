from DrawBoard import *
from Pawns import pawnsDict, initialStateOfPawns


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(tabla_a: list, start_s: tuple, end_s: tuple):
    # Pretvaranje uneteih koordinata tacaka u koordinate iz matrice tabla
    start = (start_s[0] * 2 - 1, start_s[1] * 2 - 1)
    end = (end_s[0] * 2 - 1, end_s[1] * 2 - 1)

    # Prave se pocetni cvor i krajnji
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Liste obradjenih cvorova, i cvorova koji su u redu za obradu
    closed_list = []
    open_list = []
    open_list.append(start_node)

    while len(open_list) > 0:

        # Cvor koji se trenutno obradjuje
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        # Pronadjen je cilj
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return list(map(lambda x: ((x[0] + 1) // 2, (x[1] + 1) // 2), path[::-1]))

        children = []

        # Koordinate mogucih zidova u odnosu na trenutnu pozicijiu
        walls = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        w_d = [(-1, -1), (1, 1), (-1, 1), (1, -1)]  # wall_diagonal
        positions = [(0, -2), (0, 2), (-2, 0), (2, 0),
                     (-2, -2), (2, 2), (-2, 2), (2, -2)]

        for new_position in positions:

            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Proverava se da li je cvor u opsegu
            if node_position[0] > (len(tabla_a) - 1) or node_position[0] < 0 or node_position[1] > (len(tabla_a[len(tabla_a)-1]) - 1) or node_position[1] < 0:
                continue

            # Proverava se da li postoje zidovi
            if positions.index(new_position) < 4:
                # wall_position
                w_p = (
                    current_node.position[0] + walls[positions.index(new_position)][0], current_node.position[1] + walls[positions.index(new_position)][1])
                if tabla_a[w_p[0]][w_p[1]] == " ||" or tabla_a[w_p[0]][w_p[1]] == "===" or tabla_a[w_p[0]][w_p[1]] == "||":
                    continue
            elif positions.index(new_position) >= 4 and positions.index(new_position) < 6:
                # wall_center
                w_c = (
                    current_node.position[0] + w_d[positions.index(new_position) % 4][0], current_node.position[1] + w_d[positions.index(new_position) % 4][1])
                if ((tabla_a[w_c[0] - 1][w_c[1]] == " ||" and tabla_a[w_c[0]][w_c[1] - 1] == "===") or
                    (tabla_a[w_c[0] - 1][w_c[1]] == " ||" and tabla_a[w_c[0] + 1][w_c[1]] == " ||") or
                    (tabla_a[w_c[0] + 1][w_c[1]] == " ||" and tabla_a[w_c[0]][w_c[1] + 1] == "===") or
                        (tabla_a[w_c[0]][w_c[1] - 1] == "===" and tabla_a[w_c[0]][w_c[1] + 1] == "===")):
                    continue
            else:
                w_c = (
                    current_node.position[0] + w_d[positions.index(new_position) % 4][0], current_node.position[1] + w_d[positions.index(new_position) % 4][1])
                if ((tabla_a[w_c[0] - 1][w_c[1]] == " ||" and tabla_a[w_c[0]][w_c[1] + 1] == "===") or
                    (tabla_a[w_c[0] - 1][w_c[1]] == " ||" and tabla_a[w_c[0] + 1][w_c[1]] == " ||") or
                    (tabla_a[w_c[0] + 1][w_c[1]] == " ||" and tabla_a[w_c[0]][w_c[1] - 1] == "===") or
                        (tabla_a[w_c[0]][w_c[1] - 1] == "===" and tabla_a[w_c[0]][w_c[1] + 1] == "===")):
                    continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            # Da li je dete vec obradjeno
            for closed_child in closed_list:
                if child == closed_child:
                    break
            else:
                child.g = current_node.g + 1
                child.h = abs(child.position[0] - end_node.position[0]) + \
                    abs(child.position[1] - end_node.position[1])
                child.f = child.g + child.h

                # Dete je vec na listi za obradu
                for open_node in open_list:
                    # Da li je novi put bolji od prethodnog
                    if child == open_node and child.g >= open_node.g:
                        break
                else:
                    open_list.append(child)
    return False
