import datetime
import math

def check_win(board, side):
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

def mini_max(game_s, turn, depth):
    # Game is string van 9 karakters. Vrije plaatsen zijn "_".
    depth += 1
    moves = [i for i in range(9) if game_s[i] == "_"]  # Lijst met indices van game. Available moves

    if check_win(game_s, "X"):
        print(f"X wint, bord      : {game_s}")
        return 10
    elif check_win(game_s, "O"):
        print(f"O wint, bord      : {game_s}")
        return -10

    if len(moves) == 0: # No more moves... Game Over.
        print(f"Gelijk spel,  bord  : {game_s}")
        return 0
        
    if turn == "X":
        value = -1000
        print()
        print(f"{depth*'*'} - turn {turn} - Value:", value)
        for move in moves:
            game_l = list(game_s)
            game_l[move] = "X"
            game_s = "".join(game_l)
            print(f"De zet van {turn}, bord: {game_s}, pos {move+1}")
            value = max(value, mini_max(game_s, "O", depth))
            game_l[move] = "_"
            game_s = "".join(game_l)
            print(f"{depth*'*'} - Node eval     : {game_s}, waarde: {value}")
            print("===============")
            print()
        return value
    else:
        value = 1000
        print()
        print(f"{depth*'*'} - turn {turn} - Value:", value)        
        for move in moves:
            game_l = list(game_s)
            game_l[move] = "O"
            game_s = "".join(game_l)
            print(f"De zet van {turn}, bord: {game_s}, pos {str(move+1)}")
            value = min(value, mini_max(game_s, "X", depth))
            game_l[move] = "_"
            game_s = "".join(game_l)
            print(f"{depth*'*'} - Node eval     : {game_s}, waarde: {value}")
            print("===============")
            print()
        return value

def find_best_move(board, player):
    best_move = -1000
    moves = list(board)
    for i, move in enumerate(moves):
        if move == "_":         # Vrije plaats, doe de zet
            moves[i] = player   # Doe de zet
            moves_s = "".join(moves)
            print()
            print(f"Routine BestMove-bord: {moves_s}")
            print("---------------------")
            print(f"X heeft gezet, bord: {moves_s}, pos {str(i+1)}")
            t_val = mini_max(moves_s, "O", 0)
            moves[i] = "_"
            if t_val > best_move:
                best_move = t_val
                to_move = i
    return to_move

def printBoard(bord, pos, turn):
    print()
    lbord = list(bord)
    lbord[pos] = turn
    b = "".join(lbord)
    print(f"{b[0]}|{b[1]}|{b[2]}")
    print("-+-+-")
    print(f"{b[3]}|{b[4]}|{b[5]}")
    print("-+-+-")
    print(f"{b[6]}|{b[7]}|{b[8]}")
    print()

print()        
print("======== START GAME ========")
#my_board = "XOXOOX___"
my_board = "XOXO_____"
my_turn = "X"
print("My Board", my_board)
value = find_best_move(my_board, my_turn)
print(f"Beste zet op positie: {value+1}")
printBoard(my_board, value, my_turn)