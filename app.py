from flask import Flask, jsonify, request #  imports specific objects and functions from the Flask web framework
from main import User, Game



# TODO: We will need CORS later when we connect front and back
# from flask_cors import CORS

# Define a Flask web application
app = Flask(__name__)
# CORS(app)

@app.route("/add_new_game", methods=["POST"])
def add_game():
    # Accepts POST requests with JSON data containing user_name
    user_data = request.get_json()
    # creates new instance of user
    user = User(user_data["user_name"])
    # calls method on this user to create a new game, returns user id
    user_id = user.get_or_create()
    # creates new instance of game
    game = Game(user_id)
    # start_game method gets questions from API, sets to db, and returns first question and four answers
    first_question = game.start_game()
    response = {
        "question": first_question,
        "score": 0
    }
    return jsonify(response)

@app.route("/check_answer", methods=["PUT"])
def check_answer():
    # user sends the answer, question_id (and user_id ) to the BE and it is retrieved
    # a new instance of Game is created and check_answer should be called


@app.route("/next_question/<game_id>")
def next_question():
    # user sends game_id to the BE
    # a new instance of Game is created and provide_question should be called




if __name__ == '__main__':
   app.run(debug=True)

