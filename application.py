from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import datetime

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

def check_win(board, side):
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
    return(redirect(url_for("index")))