from random import randint

DRAW1_POINTS = 4
DRAW2_POINTS = 2
WIN_POINTS = 6
LOSE_POINTS = 0
ROUNDS_NUMBER = 100

indeks_zdrady = 0


def game(player1, player2):
    points1 = 0
    points2 = 0
    moves1 = ""
    moves2 = ""
    global indeks_zdrady
    indeks_zdrady = 0
    for round_number in range(1, ROUNDS_NUMBER + 1):
        move1 = make_move(round_number, moves2, player1)
        move2 = make_move(round_number, moves1, player2)
        moves1 += move1
        moves2 += move2
        if move1 == "Z" and move2 == "Z":
            points1 += DRAW2_POINTS
            points2 += DRAW2_POINTS
        elif move1 == "Z" and move2 == "W":
            points1 += WIN_POINTS
            points2 += LOSE_POINTS
        elif move1 == "W" and move2 == "Z":
            points1 += LOSE_POINTS
            points2 += WIN_POINTS
        else:
            points1 += DRAW1_POINTS
            points2 += DRAW1_POINTS
    #print([points1, points2])
    return [points1, points2]


def make_move(round_number, opponent_previous_moves, type):
    # gracz losowy lub 1 runda
    if (type == "random" or round_number == 1):
        if randint(0, 9) % 2 == 0:
            return "Z"
        else:
            return "W"
    # naśladowca
    if type == "naśladowca":
        return opponent_previous_moves[-1]

    # zawsze zdradza, chyba że w ostatnich trzech ruchach ktoś był 2 razy wierny
    if type == "zdrajca":
        if round_number < 4:
            return "Z"
        last_three_moves = opponent_previous_moves[-3:]
        tmp = [1 if move == "Z" else 0 for move in last_three_moves]
        if sum(tmp) < 2:
            return "W"
        else:
            return "Z"

    # zawsze wierny, chyba, że w ostatnich trzech ruchach ktoś 2 razy zdradził
    if type == "wierny":
        if round_number < 4:
            return "W"
        last_three_moves = opponent_previous_moves[-3:]
        tmp = [1 if move == "Z" else 0 for move in last_three_moves]
        if sum(tmp) < 2:
            return "Z"
        else:
            return "W"
     # na początku zawsze jest wierny, potem jeśli przeciwnik w ostatnich 2 ruchach zdradził to zdradza 3 razy
    # inaczej jest wierny z prawdopodobieństwem 2/3, czasem zdarza mu się być losowym
    if(type == "mieszany"):
        global indeks_zdrady
        if(round_number < 4):
            return "W"
        if(randint(1,10) == 5):
            if(randint(1, 3) % 3 != 0):
                return "W"
            else:
                return "Z"
        if indeks_zdrady >0:
            indeks_zdrady -=1
            return "Z"
        if(opponent_previous_moves[-2] == "Z" and opponent_previous_moves[-1] == "Z"):
            indeks_zdrady = 2
            return "Z"
        if(randint(1,3) %3 !=0):
            return "Z"
        else:
            return "W"


if __name__ == "__main__":
    player1 = "mieszany"
    player2 = "zdrajca"

    player1_score = 0
    player2_score = 0
    for i in range(ROUNDS_NUMBER):
        results = game(player1, player2)
        if (results[0] > results[1]):
            player1_score += 1
        elif (results[1] > results[0]):
            player2_score += 1
        else:
            player1_score += 1
            player2_score += 1
    print("Player 1 type : " + player1 + " result : " + str(player1_score))
    print("Player 2 type : " + player2 + " result : " + str(player2_score))
