from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import datetime
import math

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

def check_win(board, side):
    print("**** - check_win routine...")
    print("**** - Board: ", board)
    print("**** - Side : ", side)

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
    print("*** - Win: ", win)
    return win

def mini_max(game, turn):
    # Game is string van 9 karakters. Vrije plaatsen zijn "_".
    moves = [i for i in range(9) if game[i] == "_"]  # Lijst met indices van game. Available moves
    print("*** - Game : ", game)
    print("*** - Moves: ", moves)
    print("*** - Turn : ", turn)

    if len(moves) == 0: # No more moves... Game Over.
        if check_win(game, "X"):
            return 1
        elif check_win(game, "O"):
            return -1
        else:
            return 0

    if turn == "X":
        value = -1 * math.inf
        print("***** - Value: ", value)
        for move in moves:
            game_t = list(game)
            print("*** - The move: ", move)
            print("*** - Game_t  : ", game_t)
            game_t[move] = "X"
            game = "".join(game_t)
            value = max(value, mini_max(game, "O"))
    else:
        value = math.inf
        print("***** - Value: ", value)        
        for move in moves:
            game_t = list(game)
            print("*** - The move: ", move)
            print("*** - Game_t  : ", game_t)            
            game_t[move] = "O"
            game = "".join(game_t)
            value = min(value, mini_max(game, "X"))

@app.route("/")
def index():
    if "board" not in session:
        session["board"] = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
        session["turn"] = "X"
        session["won"] = "_"
        session["moves"] = 0
    return(render_template("game.html", game=session["board"], turn=session["turn"], won=session["won"], moves=session["moves"]))

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    session["moves"] += 1
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
    s = ''.join(str(item) for innerlist in session["board"] for item in innerlist)
    if check_win(s, "X"):
        session["won"] = "X"
    elif check_win(s, "O"):
        session["won"] = "O"
    return(redirect(url_for("index")))

@app.route("/reset-game")
def reset_game():
    session["board"] = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
    session["turn"] = "X"
    session["won"] = "_"
    session["moves"] = 0
    return(redirect(url_for("index")))

@app.route("/computer-move")
def computer_move():
    s = ''.join(str(item) for innerlist in session["board"] for item in innerlist)
    mini_max(s, "X")
    return(redirect(url_for("index")))