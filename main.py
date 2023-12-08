import requests  # import module for requesting API
import json  # import module to work with json data
import itertools

# ANSI escape codes for colors
COLORS = {
    'red': '\033[0;31m',
    'yellow': '\033[0;33m',
    'green': '\033[0;32m',
    'blue': '\033[0;34m',
    'end': '\033[0m'
}


def print_colored_answers(answers):
    color_cycle = itertools.cycle(COLORS.keys())
    # letters = ["A", "B", "C", "D"]
    for ind, answer in enumerate(answers):
        color_name = next(color_cycle)
        color = COLORS.get(color_name)
        print(f"{color}{answer}{COLORS['end']}")


def next_question(game_id):
    result = requests.get(
        "http://127.0.0.1:5000/next_question/{}".format(game_id),
        headers={"content-type": "application/json"}
    )
    return result.json()


def fifty_fifty(question_id):
    result = requests.get(
        "http://127.0.0.1:5000/fifty_fifty/{}".format(question_id),
        headers={"content-type": "application/json"}
    )
    return result.json()


def ask_audience(question_id):
    result = requests.get(
        "http://127.0.0.1:5000/ask_audience/{}".format(question_id),
        headers={"content-type": "application/json"}
    )
    return result.json()


def add_game(user_name):
    info = {
        "user_name": user_name
    }

    result = requests.post(
        "http://127.0.0.1:5000/add_new_game",
        headers={"content-type": "application/json"},
        data=json.dumps(info)
    )
    return result.json()


def check_question(game_id, answer, question_id):
    info = {
        "game_id": game_id,
        "answer": answer,
        "question_id": question_id
    }

    result = requests.put(
        "http://127.0.0.1:5000/check_answer",
        headers={"content-type": "application/json"},
        data=json.dumps(info)
    )
    return result.json()


def show_leaderboard():
    result = requests.get(
        "http://127.0.0.1:5000/leaderboard/",
        headers={"content-type": "application/json"}
    )
    return result.json()


# BEFORE RUNNING THIS FILE REMEMBER to create a database and all the tables with the code from database.sql
# Remember to run the app.py file
# Remember to set your password in config file

def display_hints(hints, question_id):
    """Function to run all hints logic"""
    if hints > 0:
        need_hint = input("\nTo use your 50/50 hint type: 1,"
                          " to ask the audience type: 2, or to answer with no hints, please type: 3 ")
        if need_hint == "1":
            fifty_fifty_info = fifty_fifty(question_id)
            print("Please choose one answer: ")
            print_colored_answers(fifty_fifty_info['answers'])
            hints -= 1
        elif need_hint == "2":
            audience_responce = ask_audience(question_id)
            for option in audience_responce:
                print(f"{option[0]} % of the audience thinks the correct answer is {option[1]}")
            hints -= 1


def run():
    print(" #####        #     #       ###       ####### ")
    print("#     #       #     #        #             #  ")
    print("#     #       #     #        #            #   ")
    print("#     #       #     #        #           #    ")
    print("#   # #       #     #        #          #     ")
    print("#    #        #     #        #         #      ")
    print(" #### #        #####        ###       ####### ")

    hints = 3
    player = input("\nYour name is ... ")
    print(f"\n{player.capitalize()}, welcome to the Quiz!\n")
    print("You will be presented with 15 questions to test your knowledge.\n")
    print(
        "You have three 50/50 hints available, as well as three chances to ask the audience what they think the "
        "answer is :)\n")
    print("Feel free to use your hints at any moment during the quiz.")
    print("Good luck and enjoy the challenge!")

    info = add_game(player)
    error_message = info.get('message', '')
    if error_message:
        print(info["message"], ". Try again\n")
        run()
    else:
        game_id = info["game_id"]
        question = info["question"]
        # print(question)
        question_id = question["question_id"]
        print("\nQUESTION: ", question['question_text'])
        print("Please choose one answer: ")
        print_colored_answers(question['answers'])
        display_hints(hints, question_id)

        answer = input(f"To answer, either copy & paste your chosen answer, or type it (case-insensitive): ").title()
        result = check_question(game_id, answer, question['question_id'])
        print(result) #########
        correct_answer = result['result']['correct_answer']
        is_player_answer_correct = result['result']['result']
        score = result['result']['score']
        print(f"Correct Answer: {correct_answer}, Result: {is_player_answer_correct}, Score: {score}\n")
        print()

        for n in range(13):
            continue_agreement = input("To see the question press y ")
            if continue_agreement == "y":
                question = next_question(game_id)
                question_id = question["question_id"]
                print("\nQUESTION: ", question['question_text'])
                print("Please choose one answer: ")
                print_colored_answers(question['answers'])
                display_hints(hints, question_id)

                answer = input(f"To answer, either copy & paste your chosen answer, or type it (case-insensitive): ").title()
                result = check_question(game_id, answer, question['question_id'])
                print(result) #########
                correct_answer = result['result']['correct_answer']
                is_player_answer_correct = result['result']['result']
                score = result['result']['score']
                print(f"Correct Answer: {correct_answer}, Result: {is_player_answer_correct}, Score: {score}\n")
                print()
                # print(result, "\n")
        print(" ")
        print("LEADERBOARD\n")
        print(show_leaderboard())


if __name__ == '__main__':
    run()
