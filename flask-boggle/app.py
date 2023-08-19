from flask import Flask, render_template, session, request, jsonify, redirect, flash
from boggle import Boggle
import os
from datetime import datetime,timedelta

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")

# Define a route to initialize the session
@app.route("/")
def initialize_session():
    if "n_played" not in session:   #this is storing number of games played
        session["n_played"] = 0

    if "highest_score" not in session:
        session["highest_score"] = 0

                                    # Redirect to the main game route
    return redirect("/game")

# Define the main game route
@app.route("/game")
def game():
    boggle_game = Boggle() #creating instance of boggle
    board = boggle_game.make_board() #generating a new board
    session["board"] = board #stores board in session
    return render_template("board.html", board=board) #rendering board.html

@app.route("/check-word", methods=["POST"])
def check_word(): #defining check_word
    guess = request.json.get("guess") #retreiving guess and board data from the request and session
    board = session.get("board")

    if not board: #if no board returns json response indicating such
        return jsonify({"result": "No active game board."})

    boggle_game = Boggle() #creates new boggle class and checks if guess is valid
    result = boggle_game.check_valid_word(board, guess)

    # Update statistics
    if result == "ok":
        current_score = len(guess)
        if current_score > session["highest_score"]:
            session["highest_score"] = current_score
        session["n_played"] += 1

    return jsonify({
        "result": result,
        "n_played": session["n_played"],
        "highest_score": session["highest_score"]
    })

if __name__ == "__main__":
    app.run(debug=True)
