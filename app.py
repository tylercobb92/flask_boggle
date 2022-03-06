from flask import Flask, render_template, session
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "qwefasdgqwef5265aasdf"

boggle_game = Boggle()


@app.route('/')
def home():
    board = boggle_game.make_board()
    session['board'] = board

    return render_template("index.html", board=board)
