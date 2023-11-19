from api_utils import get_questions_from_api

class ConnectionError(Exception):
    pass


url = 'https://opentdb.com/api.php?amount=5&difficulty={}'


class User:

    def __init__(self, name):
        self.name = name

    def get_or_create(self):
        # With a user's name from response check in DB if user exists
        # if true - return user_id,
        # if false - write in DB a new user and return user_id
        pass


class Game:

    def __init__(self, user_id):
        self.user_id = user_id

    def start_game(self):
        # to write a new game to a database
        # TODO: realise function set_game_to_database
        # set_game_to_database(user_id)

        # to get questions from the API
        self.set_questions()

        # to get a first question
        first_question = self.provide_question()
        return first_question


    def set_questions(self):
        questions = []
        for el in ["easy", "medium", "hard"]:
            try:
                response = get_questions_from_api(url.format(el))
                questions.append(response)
            except Exception:
                raise ConnectionError("Failed to get questions from API")

        # with function imported from db_utils we will push them to db(it does not exist yet)
        # for question in questions:
        # TODO: realise function set_questions_to_db
        # set_questions_to_db(question.question, question.difficulty, question.correct_answer, question.incorrect_answers)


    # TODO: if we decide to realise the functionality when player wants to take money and go
    # def finish_game(self):
    #     pass

    def check_answer(self, question_id, user_id):
    # request is sent to db to get the right answer for this question and question's value
    # the right answer is compared with the player's answer
    # user's score is got
    # if it is correct the score is increased and returned
    # if it is wrong the game is ended score in DB is set to zero and object with score zero is returned


    def provide_question(self):
        # TODO: make request to database which returns next question and answers with this game id and where used is false
        # TODO: it also has to to set this question's used field to true
        pass

class Lifeline:

    def provide_lifeline(self):
        pass



class Fifty_Fifty(Lifeline):
    def __init__(self, question_id):
        self.question_id = question_id

    def provide_lifeline(self):
        # request to database is made, and two wrong answers are sent and returned
        # front sees them and eliminates these two
        pass


class Phone(Lifeline):
    def __init__(self, question_id):
        self.question_id = question_id
    def provide_lifeline(self):
        # request to database is made, and correct and one wrong answer is sent back
        # one is randomly chosen out of two and sent to FE
        # front shows face of Bill Gates who says this answer