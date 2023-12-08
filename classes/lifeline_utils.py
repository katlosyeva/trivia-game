from collections import deque
import random


def random_partition(target):
    """function takes the percent(usually 100) and distributes into 4 random percents, returns array of them"""
    a = random.randint(1, target - 3)
    b = random.randint(1, target - a - 2)
    c = random.randint(1, target - a - b - 1)
    d = target - a - b - c
    return [a, b, c, d]


def move_answers(answers):
    """takes answers and returns  the list like [[56, 'Bro'], [26, 'Becquerel'], [17, 'Doc Scratch'], [1, 'Halley']],
     which represents what percent of audience chooses what option. It has its algorythm.
    In 60 % of the cases the audience will be clever, most of it will vote correcty, so Bro will be the correct option.
     In 20 percent of the cases the audience will be slightly less clever and the correct answer will be second chosen,
      in 15 % of the cases - even less clever and the correct will be the third most voted option,
       in 5 - it will be not clever and the least chosen option will be correct. """
    dequed_answers = deque(answers)
    # Generate a random number between 0 and 1
    rand_num = random.random()

    # Determine the correct answer position based on the random number
    if rand_num <= 0.6:
        return dequed_answers
    elif 0.6 < rand_num < 0.8:
        dequed_answers.rotate(1)
        print("0.75", dequed_answers)
    elif 0.8 <= rand_num < 0.95:
        dequed_answers.rotate(2)
        print("0.9", dequed_answers)
    else:
        dequed_answers.rotate(3)
        print("1", dequed_answers)
    return dequed_answers
