import html
import mysql.connector  # module that allows to establish database connection
import random
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin="mysql_native_password",
        database=db_name
    )
    return connection


def get_or_add_player_id(username):
    """function which checks whether username exists and returns player_id,
    # and if username does not exist, new username is added to players and returns new player_id"""
    player_id = None
    cur = None  # Initialize cur outside the try block
    db_connection = None  # Initialize db_connection outside the try block

    try:
        # Check if username is not NULL and does not exceed 40 characters
        if username == "" or len(username) > 40:
            raise ValueError("Invalid username length. Must be 1-40 characters in length")

    except ValueError as ve:
        print(f"Invalid username: {ve}")
        return None

    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to check if player username exists
        check_query = "SELECT id FROM players WHERE username = %s"
        values = (username,)
        cur.execute(check_query, values)
        existing_player_id = cur.fetchone()

        if existing_player_id:
            # Player exists
            player_id = existing_player_id[0]
            print(f"Username '{username}' already exists in the database.")
            print(f"For existing username '{username}', player_id: {player_id}\n")
        else:
            # Player does not exist, add the new player
            add_query = "INSERT INTO players (username) VALUES (%s)"
            cur.execute(add_query, values)
            db_connection.commit()
            print("Player successfully added to DB!")

            # Get the ID of the last inserted row (player_id)
            player_id = cur.lastrowid
            print(f"For new username '{username}', new player_id: {player_id}\n")


    # except ValueError as ve:
    #     print(f"ValueError: {ve}")
    #     raise  # Re-raise the exception after printing
    #     return None

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")

    finally:
        if cur:
            # Close the cursor
            cur.close()
        if db_connection:
            # Close the connection
            db_connection.close()

        return player_id


def add_new_game(user_id):
    """DB function to add a new game to DB, returns game_id"""
    db_connection = None  # Initialize db_connection to None
    cur = None  # Initialize cur to None

    try:
        # Check if user_id is a valid integer and positive
        user_id = int(user_id)
        if user_id <= 0:
            raise ValueError("Invalid user_id. Must be a positive integer.")
    except ValueError as ve:
        # Handle the case where user_id is not a valid integer or not positive
        print(f"Invalid user_id: {ve}")
        return None

    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'games' table with score set to 0
        insert_query = "INSERT INTO games (user_id, score) VALUES (%s, 0)"
        # value to be inserted
        data = (user_id,)
        # Execute the query with the provided values
        cur.execute(insert_query, data)
        # Commit the changes to the database
        db_connection.commit()
        print("Game successfully added to DB!")

        # Get the ID of the last inserted row (game_id)
        game_id = cur.lastrowid
        print(f"add_new_game function returns game_id: {game_id}\n")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}\n")
        game_id = None  # Set game_id to None in case of an error

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")
        game_id = None  # Set game_id to None in case of an error

    finally:
        if cur:
            # Close the cursor
            cur.close()
        if db_connection:
            # Close the connection
            db_connection.close()

    return game_id


def add_new_questions(game_id, question_text, correct_answer, incorrect_answers):
    """DB function to add questions data to questions table in DB,
     takes game_id, question_text, correct_answer, incorrect_answers"""
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'questions' table
        query = """
                INSERT INTO questions (
                    game_id,
                    question,
                    correct_answer,
                    answer_1,
                    answer_2,
                    answer_3,
                    already_displayed
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

        # Tuple containing the values to be inserted
        values = (game_id,
                  html.unescape(question_text).strip(),
                  html.unescape(correct_answer).strip(),
                  html.unescape(incorrect_answers[0]).strip(),
                  html.unescape(incorrect_answers[1]).strip(),
                  html.unescape(incorrect_answers[2]).strip(),
                  False
                  )

        # Execute the query with the provided values
        cur.execute(query, values)

        # Commit the changes to the database
        db_connection.commit()
        print(f"Question successfully added to DB!")

        # Get the last inserted ID (question_id)
        question_id = cur.lastrowid
        print(f"add_new_question function returns question_id: {question_id}\n")

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}\n")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")

    finally:
        if db_connection:
            # close the connection
            db_connection.close()


def display_question_to_player(game_id):
    """DB function, that takes game_id and returns question_id, game_id, question_text and answers"""
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        print(f"Connected to database {db_name}")

        # SQL query to fetch the question details using parameterized query
        query = """
            SELECT id, game_id, question, correct_answer, answer_1, answer_2, answer_3
            FROM questions
            WHERE game_id = %s
            AND already_displayed = False
            LIMIT 1
        """
        cur.execute(query, (game_id,))
        question_displayed = cur.fetchone()

        if question_displayed is not None:
            question_id = question_displayed[0]
            game_id = question_displayed[1]
            question_text = question_displayed[2]
            answers = [question_displayed[3], question_displayed[4], question_displayed[5], question_displayed[6]]
            # answers.sort()  # sort answers in alphabetical order, which will then be shuffled in Frontend/main.py
            # later

            # SQL query to mark the question as provided using parameterized query
            query2 = """
                UPDATE questions
                SET already_displayed = True
                WHERE id = %s
            """
            cur.execute(query2, (question_id,))
            db_connection.commit()

            # fetched_question = {
            #     "question_id": question_id,
            #     "game_id": game_id,
            #     "question_text": question_text,
            #     "answers": random.sample(answers, len(answers))
            # }
            # print(f"Fetched question:\n{fetched_question}")

            return {
                "question_id": question_id,
                "game_id": game_id,
                "question_text": question_text,
                "answers": random.sample(answers, len(answers))  # randomize the order of answers, so they will be
                # displayed to player in random order
                # "answers": answers
            }
        else:
            return {"message": "No more questions"}

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}\n")
        return {"error": "An error occurred while fetching the question"}

    finally:
        if db_connection:
            cur.close()
            db_connection.close()


def display_question_to_player_fifty_fifty(question_id):
    """connects to db and returns question_id, game_id, question_text
     and two options for the question including one correct"""
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the question details
        query = """
                SELECT id, game_id, question, correct_answer, answer_1
                FROM questions
                WHERE id = %s
            """

        cur.execute(query, (question_id,))
        question_displayed = cur.fetchone()

        if question_displayed:
            question_id = question_displayed[0]
            game_id = question_displayed[1]
            question_text = question_displayed[2]
            answers = [question_displayed[3], question_displayed[4]]
            random.sample(answers,
                          len(answers))  # randomize the order of the two remaining answers to display to player

            return {
                "question_id": question_id,
                "game_id": game_id,
                "question_text": question_text,
                "answers": answers
            }
        else:
            # If question is not found, raise an exception
            raise ValueError(f"Question with ID {question_id} not found.")

    except Exception as exc:
        return {"error": str(exc)}


    finally:
        if cur:
            cur.close()  # Close the cursor if it exists
        if db_connection:
            db_connection.commit()  # Commit the changes
            db_connection.close()


def get_correct_answer(question_id):
    """takes question_id, makes request to db and returns the correct answer for this question"""
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the correct answer
        query = """
                        SELECT correct_answer
                        FROM questions
                        WHERE id = %s
                        """
        cur.execute(query, (question_id,))
        correct_answer = cur.fetchone()

        # Check if no question is found
        if correct_answer is None:
            raise ValueError(f"No question found with ID {question_id}")

        return correct_answer[0]

    except ValueError as ve:
        raise ve  # Reraise the specific ValueError

    except Exception as e:
        print(f"Failed to fetch question from DB. Error: {e}")
        raise DbConnectionError("Failed to fetch question from DB")

    finally:
        if cur:
            cur.close()  # Close the cursor if it exists
        if db_connection:
            db_connection.close()


def update_game_score(game_id):
    """DB function that takes game_id and updates the game score."""
    cur = None  # Initialize cur outside the try block

    # Check if game_id is not an integer
    if not isinstance(game_id, int):
        raise ValueError("Invalid game_id. Please provide an integer.")

    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # Query to update the score
        query_to_update_score = """
            UPDATE games
            SET score = score + 1
            WHERE id = %s
        """
        cur.execute(query_to_update_score, (game_id,))
        db_connection.commit()

    except Exception as e:
        print(f"Failed to update game score in DB. Error: {e}")
        raise DbConnectionError("Failed to update game score in DB")

    finally:
        if cur:
            cur.close()  # Close the cursor if it exists
        if db_connection:
            db_connection.close()


def get_user_score(game_id):
    """DB function, that takes game_id and returns the game score"""
    cur = None  # Initialize cur outside the try block
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the score
        query = f"""
                    SELECT score
                    FROM games
                    WHERE id = {game_id}
                """

        cur.execute(query)
        # storing the score in a variable
        score = cur.fetchone()
        return score[0]

    except Exception:
        raise DbConnectionError("Failed to fetch score from DB\n")

    finally:
        if cur:
            cur.close()  # Close the cursor if it exists
        if db_connection:
            db_connection.close()


def get_leaderboard():
    """connects to db and returns ten top scores of the players in a game and their usernames"""
    cur = None  # Initialize cur outside the try block
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the score details
        query = """
            SELECT players.username, games.score
            FROM players
            JOIN games ON players.id = games.user_id
            ORDER BY games.score DESC
        """

        cur.execute(query)
        leaderboard = cur.fetchall()

        # Return the top 10 entries if available
        return leaderboard[:10]

    except Exception:
        raise DbConnectionError("Failed to retrieve leaderboard from DB")

    finally:
        if cur:
            cur.close()  # Close the cursor if it exists
        if db_connection:
            db_connection.close()


def get_all_answers(question_id):
    """DB function, that takes question_id and returns four answers"""
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        print(f"Connected to database {db_name}")

        # SQL query to fetch the question details using parameterized query
        query = """
            SELECT correct_answer, answer_1, answer_2, answer_3
            FROM questions
            WHERE id = %s
        """
        cur.execute(query, (question_id,))
        answers = cur.fetchone()

        return answers



    except Exception:
        raise DbConnectionError("Failed to retrieve answers from DB")

    finally:
        if db_connection:
            cur.close()
            db_connection.close()


def main():
    # pass
    # Run quick tests on DB functions:
    get_or_add_player_id("Megan")
    add_new_game(1)
    add_new_questions(1, "What is the capital of France?", "Paris", ["Berlin", "Madrid", "Rome"])
    get_or_add_player_id("")
    get_or_add_player_id("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    add_new_game(-1)
    print(f"Question details for question to be displayed:\n{display_question_to_player(1)}")
    print("\n")
    print(f"Fifty/fifty answers: {display_question_to_player_fifty_fifty(1)}")
    print("\n")
    print(f"Correct answer: {get_correct_answer(1)}")
    print("\n")
    print(f"Updated game score: {update_game_score(1)}")
    print("\n")
    print(f"After score is updated, get_user_score returns score: {get_user_score(1)}")
    print("\n")
    print(f"Leaderboard Top 10:\n{get_leaderboard()}")


if __name__ == '__main__':

    # print(display_question_to_player(1))
    main()

