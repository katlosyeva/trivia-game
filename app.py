from flask import Flask, jsonify, request  # imports specific objects and functions from the Flask web framework

from classes.lifeline import FiftyFifty
from classes.lifeline import AskAudience
from classes.user import User
from classes.game import Game

# We need CORS when we connect frontend and backend
from flask_cors import CORS

# Define a Flask web application
app = Flask(__name__)

CORS(app)


@app.route("/add_new_game", methods=["POST"])
def add_game():
    """
        Endpoint to create a new game for a user.

        Expected JSON input:
        {
            "user_name": "string"
        }

        Returns:
        - {"player_id": int, "game_id": int, "question": string} if successful.
        - {"message": "Username must be between 1 and 40 characters"}, 400 if input is invalid.
        - {"message": "Internal server error"}, 500 if there's a server error.
        """

    if not request.is_json:
        return {"message": "Invalid content type. Expected JSON"}, 400

    # Accepts POST requests with JSON data containing user_name
    user_data = request.get_json()

    # Check if "user_name" is missing, empty, or longer than 40 characters
    if "user_name" not in user_data or not (1 <= len(user_data["user_name"]) <= 40):
        return {"message": "User name must be between 1 and 40 characters"}, 400

    try:
        # creates a new instance of user
        user = User(user_data["user_name"])
        # calls method on this user to create a new game, returns user id
        user_id = user.get_or_create()
        # creates a new instance of the game
        game = Game(user_id)
        # start_game method gets questions from API, sets to db, and returns the first question and four answers
        game_id = game.start_game()
        question = Game.provide_question(game_id)
        response = {
            "player_id": user_id,
            "game_id": game_id,
            "question": question
        }
        return jsonify(response)
    except Exception as e:
        # Log the exception details for debugging
        print(f"An error occurred: {str(e)}")
        return {"message": "Internal server error"}, 500


@app.route("/check_answer", methods=["PUT"])
def check_answer():
    """
    Endpoint to check whether the user-provided answer is correct for a specific game and question.

    Expected JSON input:
    {
        "game_id": int,
        "answer": "string",
        "question_id": int
    }

    Returns:
    - {"result": True} if the answer is correct.
    - {"result": False} if the answer is incorrect.
    - {"message": "Missing required fields"}, 400 if required fields are missing.
    - {"message": "Internal server error"}, 500 if there's a server error.
    """

    if not request.is_json:
        return {"message": "Invalid content type. Expected JSON"}, 400

    answer = request.get_json()

    # Validate required fields
    required_fields = ["game_id", "answer", "question_id"]
    if not all(field in answer for field in required_fields):
        return {"message": "Missing required fields"}, 400

    game_id = answer["game_id"]
    user_answer = answer["answer"]
    question_id = answer["question_id"]

    try:
        answer_was_correct = Game.check_answer(game_id, question_id, user_answer)
        return {"result": answer_was_correct}
    except Exception as e:
        # Log the exception details for debugging
        print(f"An error occurred: {str(e)}")
        return {"message": "Internal server error"}, 500


@app.route("/next_question/<game_id>")
def next_question(game_id):
    try:
        next_quest = Game.provide_question(game_id)

        if next_quest is None:
            # Game is over, return a proper JSON response with a 404 status code
            return jsonify({"error": "End of game"}), 404
        else:
            # Game is ongoing, return the next question
            return next_quest
    except Exception as e:
        # Log the exception details for debugging
        print(f"An error occurred: {str(e)}")
        return {"message": "Internal server error"}, 500


@app.route("/fifty_fifty/<question_id>")
def updated_question(question_id):
    try:
        updated_quest = FiftyFifty.provide_lifeline(question_id)
        return updated_quest
    except Exception as e:
        # Log the exception details for debugging
        print(f"An error occurred: {str(e)}")
        return {"message": "Internal server error"}, 500


@app.route("/ask_audience/<question_id>")
def get_audience_choice(question_id):
    try:
        audience_choice = AskAudience.provide_lifeline(question_id)
        return audience_choice
    except Exception as e:
        # Log the exception details for debugging
        print(f"An error occurred: {str(e)}")
        return {"message": "Internal server error"}, 500


@app.route("/leaderboard/")
def show_leaderboard():
    try:
        leaderboard = Game.show_leaderboard()
        return leaderboard
    except Exception as e:
        # Log the exception details for debugging
        print(f"An error occurred: {str(e)}")
        return {"message": "Internal server error"}, 500


if __name__ == '__main__':
    app.run(debug=True)
