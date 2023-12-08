from api_utils import get_questions_from_api
import html

from db_utils import add_new_game, add_new_questions, display_question_to_player, get_correct_answer, update_game_score, \
    get_user_score, display_question_to_player_fifty_fifty, get_leaderboard


class Game:

    def __init__(self, user_id):
        self.user_id = user_id

    def start_game(self):
        """""method sets the new game to the db, returns the game_id"""

        # to write a new game to a database
        game_id = add_new_game(self.user_id)

        # to get question from the API
        self.set_questions(game_id)

        return game_id


    @staticmethod
    def set_questions(game_id):
        """method takes game_id and makes request to the third-party API to get 15 questions, which later sets to the
        db"""
        try:
            questions = get_questions_from_api('https://opentdb.com/api.php?amount=15&type=multiple')["results"]
        except Exception:
            raise ConnectionError("Failed to get questions from API")
        # setting questions one by one to the db
        for question in questions:
            add_new_questions(game_id, question["question"], question["correct_answer"], question["incorrect_answers"])

    @staticmethod
    def check_answer(game_id, question_id, user_answer):
        """method takes game_id, question_id, user_answer as parameters,
        gets the correct answer from the db and checks it with the player's answer,
        updates player's score and returns score, correct answer and string wrong/correct"""

        # request is sent to db to get the right answer for this question and question's value
        correct_answer = get_correct_answer(question_id)
        # the right answer is compared with the player's answer
        if user_answer == html.unescape(correct_answer):
            # if it is correct the score is increased and returned
            update_game_score(game_id)
            user_score = get_user_score(game_id)

            return {"score": user_score, "correct_answer": correct_answer, "result": "correct"}
        else:
            # user's score is got
            previous_score = get_user_score(game_id)
            return {"score": previous_score, "correct_answer": correct_answer, "result": "wrong"}

    @staticmethod
    def provide_question(game_id):
        """"method takes one parameter game_id and returns the question from the database"""
        result = display_question_to_player(game_id)
        return result

    # @staticmethod
    # def fifty_fifty(question_id):
    #
    #     result = display_question_to_player_fifty_fifty(question_id)
    #     return result

    @staticmethod
    def show_leaderboard():
        """method shows returns ten top results of players and their usernames"""
        result = get_leaderboard()
        return result


if __name__ == '__main__':
    game = Game(1)
    game.set_questions(1)
    print(game.fifty_fifty(57))
