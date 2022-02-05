from StateOfTheBoard import allValidStates


def checkValue(stanje):
    score = 0
    for i in range(0, 2):
        current_pos = stanje[1]['X'][i]
        end0 = stanje[1]['startO'][0]
        end1 = stanje[1]['startO'][1]

        allWalls = stanje[2]['V']
        allWalls.extend(stanje[2]['H'])
        for wall in allWalls:
            if(wall[0] >= min(current_pos[0], end0[0]) and wall[0] <= max(current_pos[0], end0[0]) and wall[1] >= min(current_pos[1], end0[1]) and wall[1] <= max(current_pos[1], end0[1])):
                score += 20
            if(wall[0] >= min(current_pos[0], end1[0]) and wall[0] <= max(current_pos[0], end1[0]) and wall[1] >= min(current_pos[1], end1[1]) and wall[1] <= max(current_pos[1], end1[1])):
                score += 20

        distance0 = abs((current_pos[0] - end0[0]) +
                        (current_pos[1] - end0[1]))
        distance1 = abs((current_pos[0] - end1[0]) +
                        (current_pos[1] - end1[1]))

        temp = min(distance0, distance1)
        if(temp == 2):
            score += 50
        elif(temp == 1):
            score += 100
        else:
            score += temp

    for i in range(0, 2):
        current_pos = stanje[1]['O'][i]
        end0 = stanje[1]['startX'][0]
        end1 = stanje[1]['startX'][1]

        allWalls = stanje[2]['V']
        allWalls.extend(stanje[2]['H'])
        for wall in allWalls:
            if(wall[0] >= min(current_pos[0], end0[0]) and wall[0] <= max(current_pos[0], end0[0]) and wall[1] >= min(current_pos[1], end0[1]) and wall[1] <= max(current_pos[1], end0[1])):
                score -= 20
            if(wall[0] >= min(current_pos[0], end1[0]) and wall[0] <= max(current_pos[0], end1[0]) and wall[1] >= min(current_pos[1], end1[1]) and wall[1] <= max(current_pos[1], end1[1])):
                score -= 20

        distance0 = abs((current_pos[0] - end0[0]) +
                        (current_pos[1] - end0[1]))
        distance1 = abs((current_pos[0] - end1[0]) +
                        (current_pos[1] - end1[1]))
        temp = min(distance0, distance1)
        if(temp == 2):
            score -= 50
        elif(temp == 1):
            score -= 100
        else:
            score -= temp

    return score


def minimax3(state, depth, maximizingPlayer, tableSizeN, tableSizeM, alpha, beta, potez=None):

    if depth == 3:
        return (potez, checkValue(state))

    igrac = "X" if maximizingPlayer else "O"
    all_states = allValidStates(
        state[0], state[1], state[2], igrac, 1, tableSizeN, tableSizeM)
    all_states.extend(allValidStates(
        state[0], state[1], state[2], igrac, 2, tableSizeN, tableSizeM))

    if all_states is None or len(all_states) == 0:
        return (potez, checkValue(state))

    if maximizingPlayer:
        best = (("min"), -1000)

        for new_state in all_states:

            val = minimax3(new_state, depth + 1,
                           False, tableSizeN, tableSizeM, alpha, beta, new_state if potez is None else potez)
            best = max(best, val, key=lambda x: x[1])
            alpha = max(alpha, best, key=lambda x: x[1])

            if beta[1] <= alpha[1]:
                break

        return best

    else:
        best = (("max"), 1000)

        for new_state in all_states:

            val = minimax3(new_state, depth + 1,
                           True, tableSizeN, tableSizeM, alpha, beta, new_state if potez is None else potez)
            best = min(best, val, key=lambda x: x[1])
            beta = min(beta, best, key=lambda x: x[1])

            if beta[1] <= alpha[1]:
                break

        return best
