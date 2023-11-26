from flask import Flask, jsonify, request  # imports specific objects and functions from the Flask web framework
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


@app.route("/check_answer", methods=["PUT"])
def check_answer():
    answer = request.get_json()
    game_id = answer["game_id"]
    user_answer = answer["answer"]
    question_id = answer["question_id"]
    answer_was_correct = Game.check_answer(game_id, question_id, user_answer)
    print(game_id, user_answer, question_id)
    return answer_was_correct


@app.route("/next_question/<game_id>")
def next_question(game_id):
    next_quest = Game.provide_question(game_id)
    if next_quest is None:
        response = jsonify({'error': 'End of game'})
        response.status_code = 404
        return response
    else:
        return next_quest


@app.route("/fifty_fifty/<question_id>")
def updated_question(question_id):
    updated_quest = Game.fifty_fifty(question_id)
    return updated_quest


if __name__ == '__main__':
    app.run(debug=True)

