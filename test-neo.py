import datetime
import math

def showBoard(board):
    print()
    print(f"{board[0]}|{board[1]}|{board[2]}")
    print("-+-+-")
    print(f"{board[3]}|{board[4]}|{board[5]}")
    print("-+-+-")
    print(f"{board[6]}|{board[7]}|{board[8]}")
    print()

def evalueer_bord(board, side):
    # Board is string van 9 karakters. Vrije plaatsen zijn "_".
    win = False
    rows = (board[:3] == side*3) or (board[3:6] == side*3) or (board[-3:] == side*3)
    cols = (board[0] == side and board[3] == side and board[6] == side) or \
           (board[1] == side and board[4] == side and board[7] == side) or \
           (board[2] == side and board[5] == side and board[8] == side)
    cross = (board[0] == side and board[4] == side and board[8] == side) or \
            (board[2] == side and board[4] == side and board[6] == side)
    if rows:
        win = True
    elif cols:
        win = True
    elif cross:
        win = True
    return win

#def heur_eval(board, side):
def heur_eval(place, side):
    ## Bepaal een extra score voor zetten op specifieke plaatsen op het bord
    v = 0
    # 2 Plaatsen: naast, onder of boven elkaar?
    # Hoekveld?
    #if board[0]==side or board[2]==side or board[6]==side or board[8]==side:
    if place == 0 or place == 2 or place == 6 or place == 8:
        v += 1
    # Middenveld?
    #if board[4]==side:
    if place == 4:
        v += 3
    # else:
    #   return 0
    return v if side=="X" else v*-1

def mini_max(game_s, turn, depth):
    # Game is string van 9 karakters. Vrije plaatsen zijn "_".
    depth += 1
    moves = [i for i in range(9) if game_s[i] == "_"]  # Lijst met indices van game. Available moves

    if evalueer_bord(game_s, "X"):   # Heeft X gewonnen?
        return 10 
    elif evalueer_bord(game_s, "O"): # Heeft O gewonnen?
        return -10

    if len(moves) == 0: # Geen zetten meer. Game Over...
        return 0
        
    if turn == "X":
        value = -1000
        #print()
        #print(f"{depth*'*'} - turn {turn} - Value:", value)
        for move in moves:
            game_l = list(game_s)
            game_l[move] = "X"
            game_s = "".join(game_l)
            #print(f"De zet van {turn}, bord: {game_s}, pos {move+1}")
            value = max(value, mini_max(game_s, "O", depth))
            game_l[move] = "_"
            game_s = "".join(game_l)
            #print(f"{depth*'*'} - Node eval     : {game_s}, waarde: {value}")
            #print("===============")
            #print()
        return value
    else:
        value = 1000
        #print()
        #print(f"{depth*'*'} - turn {turn} - Value:", value)        
        for move in moves:
            game_l = list(game_s)
            game_l[move] = "O"
            game_s = "".join(game_l)
            #print(f"De zet van {turn}, bord: {game_s}, pos {str(move+1)}")
            value = min(value, mini_max(game_s, "X", depth))
            game_l[move] = "_"
            game_s = "".join(game_l)
            #print(f"{depth*'*'} - Node eval     : {game_s}, waarde: {value}")
            #print("===============")
            #print()
        return value

def find_best_move(board, player):
    best_move = -1000
    moves = list(board)
    for i, move in enumerate(moves):
        if move == "_":         # Vrije plaats, doe de zet
            moves[i] = player   # Doe de zet
            moves_s = "".join(moves)
            player = "X" if player == "O" else "O" # Bepaals volgende speler
            #print()
            #print(f"Routine BestMove-bord: {moves_s}")
            #print("---------------------")
            #print(f"X heeft gezet, bord: {moves_s}, pos {str(i+1)}")
            t_val = mini_max(moves_s, player, 0) # Bepaal de score, recursief
            t_val += heur_eval(i, "X")        # Voeg heuristische waarde toe
            moves[i] = "_"
            print(f"Best value: {best_move}, berekend: {t_val}")
            if t_val > best_move:
                best_move = t_val
                to_move = i
    return to_move

def zet_voor_x(board, turn):
    pos = find_best_move(board, "X")
    b = list(board)
    b[pos] = "X"
    return "".join(b)

def zet_voor_o(board, turn):
    print()
    m = int(input("Positie om te zetten (1 - 9)? "))
    b = list(board)
    while (m<1 or m>9) or (b[m-1] != "_"):
        m = int(input("Alleen vrije posities tussen (1 - 9)? "))
        b = list(board)
    b[m-1] = "O"
    return "".join(b)

print()        
print("======== START GAME ========")
#my_board = "XOXOOX___"
my_board = "_________"
my_turn = "X"
showBoard(my_board)
for m in range(1,10):
    if my_turn == "X":
        my_board = zet_voor_x(my_board, my_turn)
        my_turn = "O"
    else:
        my_board = zet_voor_o(my_board, my_turn)
        my_turn = "X"
    showBoard(my_board)
    if evalueer_bord(my_board, "X"):
        print("X heeft gewonnen!")
        break
    if evalueer_bord(my_board, "O"):
        print("O heeft gewonnen!")
        break
    if "_" not in my_board:
        print("Het is remise...")
        break
print()