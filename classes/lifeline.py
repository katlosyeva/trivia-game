from db_utils import display_question_to_player_fifty_fifty, get_all_answers
from .lifeline_utils import random_partition, move_answers


class Lifeline:
    @staticmethod
    def provide_lifeline(question_id):
        pass


class FiftyFifty(Lifeline):
    @staticmethod
    def provide_lifeline(question_id):
        result = display_question_to_player_fifty_fifty(question_id)
        return result


class AskAudience(Lifeline):
    @staticmethod
    def provide_lifeline(question_id):
        answers = get_all_answers(question_id)
        percentages = random_partition(100)
        percentages.sort(reverse=True)
        answers_in_new_order = move_answers(answers)

        # Create a list of tuples with percentages and answers
        data = list(zip(percentages, answers_in_new_order))

        return data

# print(AskAudience.provide_lifeline(5))
