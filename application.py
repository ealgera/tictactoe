from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import datetime
import math

import minimax  # Mijn Mini-Max algoritme

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

@app.route("/")
def index():
    if "board" not in session:
        session["board"] = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
        session["turn"] = "X"
        session["won"] = "_"
        session["moves"] = 0
    return(render_template("game.html", game=session["board"], turn=session["turn"], \
                                        won=session["won"], moves=session["moves"]))

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    session["moves"] += 1
    print("Route Play")
    print(f"Zetten: {session['moves']}, Bord: {session['board']}")
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
    s = ''.join(str(item) for innerlist in session["board"] for item in innerlist)
    if minimax.evalueer_bord(s, "X"):
        session["won"] = "X"
    elif minimax.evalueer_bord(s, "O"):
        session["won"] = "O"
    if session["moves"] <=8:
        computer_move()
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
    # Bepaal beste zet voor de computer. find_best_move(board, player)
    print(f"Bord: {s} en zet voor {session['turn']}")
    pos = minimax.find_best_move(s, session['turn'])
    pos_row = pos % 3
    pos_col = pos // 3
    print(f"Beste zet op positie: {pos+1}, dat is: {pos_row}-{pos_col}")
    #redirect(url_for("play", row=pos_row, col=pos_col))
    session["board"][pos_col][pos_row] = session["turn"]
    session["moves"] += 1
    session["turn"] = "X" if session["turn"] == "O" else "O"
    s = ''.join(str(item) for innerlist in session["board"] for item in innerlist)
    if minimax.evalueer_bord(s, "X"):
        session["won"] = "X"
    elif minimax.evalueer_bord(s, "O"):
        session["won"] = "O"
    return(redirect(url_for("index")))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
