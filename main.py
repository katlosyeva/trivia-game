import requests  # import module for requesting API
import json  # import module to work with json data


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
def run():
    hints = 2
    player = input("Your name is ...")
    info = add_game(player)
    game_id = info["game_id"]
    question = info["question"]
    question_id = question["question_id"]
    print("The question: ", question['question_text'])
    print("Answers: ", question['answers'])
    if hints > 0:
        need_hint = input("Would you use 50/50? (y/n)")
        if need_hint == "y":
            fifty_fifty_info = fifty_fifty(question_id)
            print("Answers: ", fifty_fifty_info['answers'])
            hints -= 1

    answer = input(f"Write the answer: ")
    result = check_question(game_id, answer, question['question_id'])
    print(result)
    for n in range(13):
        continue_agreement = input("To see the question press y")
        if continue_agreement == "y":
            question = next_question(game_id)

            print("The question: ", question['question_text'])
            print("Answers: ", question['answers'])
            if hints > 0:
                need_hint = input("Would you use 50/50? (y/n)")
                if need_hint == "y":
                    fifty_fifty_info = fifty_fifty(question_id)
                    print("Answers: ", fifty_fifty_info['answers'])
                    hints -= 1

            answer = input(f"Write the answer: ")

            result = check_question(game_id, answer, question['question_id'])
            print(result)
    print(" ")
    print("LEADERBOARD\n")
    print(show_leaderboard())


if __name__ == '__main__':
    run()
