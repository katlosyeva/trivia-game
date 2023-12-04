from flask import Flask, jsonify, request  # imports specific objects and functions from the Flask web framework

from classes.lifeline import FiftyFifty
from classes.user import User
from classes.game import Game

# We need CORS when we connect front and back
from flask_cors import CORS

# Define a Flask web application
app = Flask(__name__)

CORS(app)


@app.route("/add_new_game", methods=["POST"])
def add_game():
    # Accepts POST requests with JSON data containing user_name
    user_data = request.get_json()
    if not user_data["user_name"]:
        return {"message": "User has to have a valid name"}, 400
    if len(user_data["user_name"]) >= 40:
        return {"message": "Username has to be less than 40 characters long"}, 400
    try:
        # creates new instance of user
        user = User(user_data["user_name"])
        # # calls method on this user to create a new game, returns user id
        user_id = user.get_or_create()
        # creates new instance of game
        game = Game(user_id)
        # # start_game method gets questions from API, sets to db, and returns first question and four answers
        game_id = game.start_game()
        question = Game.provide_question(game_id)
        response = {
            "player_id": user_id,
            "game_id": game_id,
            "question": question
        }
        #
        return jsonify(response)
    except Exception:
        return {"message": "Internal server error"}, 500


@app.route("/check_answer", methods=["PUT"])
def check_answer():
    answer = request.get_json()
    game_id = answer["game_id"]
    user_answer = answer["answer"]
    question_id = answer["question_id"]
    try:
        answer_was_correct = Game.check_answer(game_id, question_id, user_answer)
        return answer_was_correct
    except Exception:
        return {"message": "Internal server error"}, 500



@app.route("/next_question/<game_id>")
def next_question(game_id):
    try:
        next_quest = Game.provide_question(game_id)
        return next_quest
    except Exception:
        return {"message": "Internal server error"}, 500




@app.route("/fifty_fifty/<question_id>")
def updated_question(question_id):
    try:
        updated_quest = FiftyFifty.fifty_fifty(question_id)
        return updated_quest
    except Exception:
        return {"message": "Internal server error"}, 500


@app.route("/leaderboard/")
def show_leaderboard():
    try:
        leaderboard = Game.show_leaderboard()
        return leaderboard
    except Exception:
        return {"message": "Internal server error"}, 500


if __name__ == '__main__':
    app.run(debug=True)
