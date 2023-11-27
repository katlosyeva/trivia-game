from api_utils import get_questions_from_api

from db_utils import add_new_game, add_new_questions, display_question_to_player, get_correct_answer, update_game_score, \
    get_user_score, display_question_to_player_fifty_fifty, get_leaderboard



class Game:

    def __init__(self, user_id):
        self.user_id = user_id

    def start_game(self):

        # to write a new game to a database
        game_id = add_new_game(self.user_id, 0)

        # to get question from the API
        self.set_questions(game_id)

        return game_id

    def set_questions(self, game_id):

        try:
            questions = get_questions_from_api('https://opentdb.com/api.php?amount=15&type=multiple')["results"]
        except Exception:
            raise ConnectionError("Failed to get questions from API")

        for question in questions:
            add_new_questions(game_id, question["question"], question["correct_answer"], question["incorrect_answers"])

    @staticmethod
    def check_answer(game_id, question_id, user_answer):
        # request is sent to db to get the right answer for this question and question's value
        # the right answer is compared with the player's answer
        # user's score is got
        # if it is correct the score is increased and returned
        correct_answer = get_correct_answer(question_id)

        if user_answer == correct_answer:
            user_score = update_game_score(game_id)
            return {"score": user_score, "correct_answer": correct_answer, "result": "correct"}
        else:
            previous_score = get_user_score(game_id)
            return {"score": previous_score, "correct_answer": correct_answer, "result": "wrong"}

    @staticmethod
    def provide_question(game_id):
        result = display_question_to_player(game_id)
        return result

    @staticmethod
    def fifty_fifty(question_id):
        result = display_question_to_player_fifty_fifty(question_id)
        return result


if __name__ == '__main__':
    game = Game(1)
    game.set_questions(1)
    print(game.fifty_fifty(57))
