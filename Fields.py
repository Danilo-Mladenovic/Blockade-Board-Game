fieldsDict = {
}


def initialStateOfFields(dictionary: dict, m: int, n: int):
    for i in range(0, m):
        for j in range(0, n):
            if i == 0:
                if j == 0:
                    dictionary[(i, j)] = [(i, j+1), (i+1, j+1), (i+1, j)]
                elif j == n-1:
                    dictionary[(i, j)] = [(i, j-1), (i+1, j), (i+1, j-1)]
                else:
                    dictionary[(i, j)] = [(i, j-1), (i+1, j),
                                          (i+1, j-1), (i, j+1), (i+1, j+1)]
            elif i == m-1:
                if j == 0:
                    dictionary[(i, j)] = [(i-1, j), (i-1, j+1), (i, j+1)]
                elif j == n-1:
                    dictionary[(i, j)] = [(i-1, j), (i, j-1), (i-1, j-1)]
                else:
                    dictionary[(i, j)] = [(i-1, j), (i, j-1),
                                          (i-1, j-1), (i-1, j+1), (i, j+1)]
            elif i != 0 and i != m-1:
                if j == 0:
                    dictionary[(i, j)] = [(i-1, j), (i-1, j+1),
                                          (i, j+1), (i+1, j+1), (i+1, j)]
                elif j == n-1:
                    dictionary[(i, j)] = [(i-1, j), (i-1, j-1),
                                          (i, j-1), (i+1, j-1), (i+1, j)]
                else:
                    dictionary[(i, j)] = [(i-1, j), (i-1, j-1),
                                          (i, j-1), (i+1, j-1), (i+1, j), (i-1, j+1), (i, j+1), (i+1, j+1)]


initialStateOfFields(fieldsDict, 4, 3)
