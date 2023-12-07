from db_utils import display_question_to_player_fifty_fifty, get_all_answers
from .lifeline_utils import random_partition, move_answers


class Lifeline:
    """Base class for lifeline functionality."""
    @staticmethod
    def provide_lifeline(question_id):
        """Provide a lifeline for the given question."""
        pass


class FiftyFifty(Lifeline):
    """Type of LifeLine class."""
    @staticmethod
    def provide_lifeline(question_id):
        """Method that takes question_id and returns two options instead of four."""
        result = display_question_to_player_fifty_fifty(question_id)
        return result


class AskAudience(Lifeline):
    """Type of LifeLine class."""
    @staticmethod
    def provide_lifeline(question_id):
        """Method that takes question_id and returns the array of what percent of audience votes for what option"""
        answers = get_all_answers(question_id)
        percentages = random_partition(100)
        percentages.sort(reverse=True)
        answers_in_new_order = move_answers(answers)

        # Create a list of tuples with percentages and answers
        data = list(zip(percentages, answers_in_new_order))

        return data

# print(AskAudience.provide_lifeline(5))
