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

def heur_eval(positie, side):
    ## Bepaal een extra score voor zetten op specifieke plaatsen op het bord
    v = 0
    # 2 Plaatsen: naast, onder of boven elkaar? Nog te bepalen
    # Hoekveld?
    if positie == 0 or positie == 2 or positie == 6 or positie == 8:
        v += 1
    # Middenveld?
    if positie == 4:
        v += 3
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
        value = -1000  # X moet een maximale waarde bepalen
        for move in moves:
            game_l = list(game_s)
            game_l[move] = "X"
            game_s = "".join(game_l)
            value = max(value, mini_max(game_s, "O", depth))
            game_l[move] = "_"
            game_s = "".join(game_l)
        return value
    else:
        value = 1000   # O moet een minimale waarde bepalen    
        for move in moves:
            game_l = list(game_s)
            game_l[move] = "O"
            game_s = "".join(game_l)
            value = min(value, mini_max(game_s, "X", depth))
            game_l[move] = "_"
            game_s = "".join(game_l)
        return value

def find_best_move(board, player):
    # Board is een string van 9 karakters. Vrije plaatsen zijn "_".
    best_move = -1000 if player == "X" else 1000 # Startwaarde Min of Max. X = Max, O = Min
    moves = list(board)
    for i, move in enumerate(moves):
        if move == "_":         # Vrije plaats
            moves[i] = player   # Doe de zet
            moves_s = "".join(moves)
            the_player = "X" if player == "O" else "O" # Bepaal volgende speler voor MiniMax
            t_val = mini_max(moves_s, the_player, 0)   # Bepaal de score volgende speler, recursief
            t_val += heur_eval(i, player)              # Voeg heuristische waarde huidige speler toe
            moves[i] = "_"     # Maak zet ongedaan
            if player == "X":  # Bepaal grootste score
                if t_val > best_move:
                    best_move = t_val
                    to_move = i
            else:              # Bepaal kleinste score
                if t_val < best_move:
                    best_move = t_val
                    to_move = i
    return to_move

def zet_voor_comp(board, turn):
    print("Ik ben aan zet...")
    pos = find_best_move(board, turn)
    b = list(board)
    b[pos] = turn
    print(f"Ik heb gezet op {pos+1}!")
    return "".join(b)

def zet_voor_mens(board, turn):
    print()
    print("Jij bent aan zet...")
    m = int(input("Positie om te zetten (1 - 9)? "))
    b = list(board)
    while (m<1 or m>9) or (b[m-1] != "_"):
        m = int(input("Alleen vrije posities tussen (1 - 9)? "))
        b = list(board)
    b[m-1] = turn
    return "".join(b)

print()        
print("======== START GAME ========")
print()

het_bord = "_________"
is_aan_zet = "X"
comp_heeft_X = True

mens = input("Wil je 'X' of 'O'? ")
while (mens.lower() != "x") and (mens.lower() != "o"):
    mens = input("Kies 'X' of 'O', welke wil je? ")

if mens.lower() == "x":
    comp_heeft_X = False

showBoard(het_bord) # Eerste, lege bord

for m in range(1,10):
    if is_aan_zet == "X":
        if comp_heeft_X:
            het_bord = zet_voor_comp(het_bord, is_aan_zet)
        else:
            het_bord = zet_voor_mens(het_bord, is_aan_zet)
        is_aan_zet = "O"
    else:
        if not comp_heeft_X:
            het_bord = zet_voor_comp(het_bord, is_aan_zet)
        else:
            het_bord = zet_voor_mens(het_bord, is_aan_zet)    
        is_aan_zet = "X"
    showBoard(het_bord)

    if evalueer_bord(het_bord, "X"):
        print("X heeft gewonnen!")
        break
    if evalueer_bord(het_bord, "O"):
        print("O heeft gewonnen!")
        break
    if "_" not in het_bord:
        print("Het is remise...")
        break
print()