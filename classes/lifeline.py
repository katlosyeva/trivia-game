from db_utils import display_question_to_player_fifty_fifty


class Lifeline:

    def provide_lifeline(self):
        pass


class FiftyFifty(Lifeline):
    def __init__(self, question_id):
        self.question_id = question_id

    @staticmethod
    def fifty_fifty(question_id):
        result = display_question_to_player_fifty_fifty(question_id)
        return result
#
#
# class Phone(Lifeline):
#     def __init__(self, question_id):
#         self.question_id = question_id
#     def provide_lifeline(self):
#         # request to database is made, and correct and one wrong answer is sent back
#         # one is randomly chosen out of two and sent to FE
#         # front shows face of Bill Gates who says this answer
