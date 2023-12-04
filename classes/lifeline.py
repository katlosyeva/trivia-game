from db_utils import display_question_to_player_fifty_fifty, get_all_answers
from collections import deque
import random


def random_partition(target):
    a = random.randint(1, target - 3)
    b = random.randint(1, target - a - 2)
    c = random.randint(1, target - a - b - 1)
    d = target - a - b - c
    return [a, b, c, d]


def move_answers(answers):
    dequed_answers = deque(answers)
    # Generate a random number between 0 and 1
    rand_num = random.random()

    # Determine the correct answer position based on the random number
    if rand_num < 0.5:
        return dequed_answers
    elif 0.5 < rand_num < 0.75:
        dequed_answers.rotate(1)
        print("0.75", dequed_answers)
    elif 0.75 < rand_num < 0.9:
        dequed_answers.rotate(2)
        print("0.9", dequed_answers)
    else:
        dequed_answers.rotate(3)
        print("1", dequed_answers)
    return dequed_answers




class Lifeline:
    @staticmethod
    def provide_lifeline(question_id):
        pass


class FiftyFifty(Lifeline):
    # def __init__(self, question_id):
    #     self.question_id = question_id

    @staticmethod
    def fifty_fifty(question_id):
        result = display_question_to_player_fifty_fifty(question_id)
        return result


class AskAudience(Lifeline):
    # def __init__(self, question_id):
    #     self.question_id = question_id

    @staticmethod
    def provide_lifeline(question_id):
        answers = get_all_answers(question_id)

        percentages = random_partition(100)
        percentages.sort(reverse=True)
        answers_in_new_order = move_answers(answers)

        # Create a list of tuples with percentages and answers
        data = list(zip(percentages, answers_in_new_order))

        return data



print(AskAudience.provide_lifeline(4))
