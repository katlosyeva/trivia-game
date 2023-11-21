import mysql.connector  # module that allows to establish database connection
from config import USER, PASSWORD, HOST
import sys


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


def check_player_exists(username):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to check if player username exists
        query = "SELECT username FROM players where username = %s"

        # values to be checked
        values = (username,)

        # Execute the query with the provided values
        cur.execute(query, values)

        # Fetch the result (customer ID) from the query
        result = cur.fetchone()

        if result:
            # Player exists
            print(f"Username {username} already exists in the database.")
            return True
        else:
            # Player does not exist
            print(f"Username {username} does not exist in the database.")
            return False

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except Exception as e:
        raise DbConnectionError("Failed to check if the player exists in the database")
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

    finally:
        if cur:
            # Close the cursor
            cur.close()
        if db_connection:
            # close the connection
            db_connection.close()


def add_new_player(username):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'players' table
        query = """
                INSERT INTO players (
                    username
                ) VALUES (%s)
                """

        # values to be inserted
        values = (username,)

        # Execute the query with the provided values
        cur.execute(query, values)

        # Commit the changes to the database
        db_connection.commit()
        print("Player successfully added to DB!")

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

    finally:
        if db_connection:
            # close the connection
            db_connection.close()


def add_new_game(player_id):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'games' table
        query = """
                INSERT INTO games (
                    player_id
                ) VALUES (%s)
                """

        # values to be inserted
        values = (player_id,)

        # Execute the query with the provided values
        cur.execute(query, values)

        # Commit the changes to the database
        db_connection.commit()
        print("Game successfully added to DB!")

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

    finally:
        if db_connection:
            # close the connection
            db_connection.close()


def add_new_questions(game_id, player_id, difficulty_level, question_text, correct_answer, incorrect_answer_1,
                      incorrect_answer_2, incorrect_answer_3):
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
                    player_id,
                    difficulty_level,
                    question_text,
                    correct_answer,
                    incorrect_answer_1,
                    incorrect_answer_2,
                    incorrect_answer_3
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

        # Tuple containing the values to be inserted
        values = (
            game_id,
            player_id,
            difficulty_level,
            question_text,
            correct_answer,
            incorrect_answer_1,
            incorrect_answer_2,
            incorrect_answer_3
        )

        # Execute the query with the provided values
        cur.execute(query, values)

        # Commit the changes to the database
        db_connection.commit()
        print(f"Question successfully added to DB!")  # MAYBE ADD PLACEHOLDER TO DISPLAY QUESTION_ID?

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

    finally:
        if db_connection:
            # close the connection
            db_connection.close()


def start_game_questions(game_id, player_id, question_id, player_answer, correct_answer, is_correct):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'game_questions' table
        query = """
                INSERT INTO game_questions (
                    game_id,
                    player_id,
                    question_id,
                    player_answer,
                    correct_answer,
                    is_correct
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """

        # Tuple containing the values to be inserted
        values = (
            game_id,
            player_id,
            question_id,
            player_answer,
            correct_answer,
            is_correct
        )

        # Execute the query with the provided values
        cur.execute(query, values)

        # Commit the changes to the database
        db_connection.commit()
        print(f"Game question successfully added to DB!")

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

    finally:
        if db_connection:
            # close the connection
            db_connection.close()


def start_game_scoreboard(game_id, player_id, total_score):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'scoreboard' table
        query = """
                INSERT INTO scoreboard (
                    game_id,
                    player_id,
                    total_score
                ) VALUES (%s, %s, %s)
                """

        # Tuple containing the values to be inserted
        values = (
            game_id,
            player_id,
            total_score
        )

        # Execute the query with the provided values
        cur.execute(query, values)

        # Commit the changes to the database
        db_connection.commit()
        print(f"Initial start score of zero successfully added to DB!")

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

    finally:
        if db_connection:
            # close the connection
            db_connection.close()


def update_player_answer_is_correct(game_id, player_id, question_id, player_answer):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # Retrieve the correct answer for the given question from the game_questions table
        cur.execute("SELECT correct_answer FROM game_questions WHERE game_id = %s AND player_id = %s "
                    "AND question_id = %s",
                    (game_id, player_id, question_id))
        correct_answer_from_db = cur.fetchone()[0]

        # Compare player's answer with the correct answer and update is_correct
        is_correct = player_answer == correct_answer_from_db

        # SQL query for updating a row in the 'game_questions' table
        update_query = """
            UPDATE game_questions
            SET
                player_answer = %s,
                is_correct = %s
            WHERE
                game_id = %s
                AND player_id = %s
                AND question_id = %s
        """

        # Tuple containing the values to be updated
        values = (player_answer, is_correct, game_id, player_id, question_id)

        # Execute the update query with the provided values
        cur.execute(update_query, values)

        # Commit the changes to the database
        db_connection.commit()
        print("Game question updated successfully!")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

    finally:
        if db_connection:
            # Close the connection
            db_connection.close()


# Example usage


def update_scoreboard_total_score(game_id, player_id):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to update total_score in the scoreboard table
        update_query = """
                UPDATE scoreboard sb
                SET total_score = (
                    SELECT SUM(CAST(gq.is_correct AS SIGNED))
                    FROM game_questions gq
                    WHERE gq.game_id = sb.game_id AND gq.player_id = sb.player_id
                )
                WHERE sb.game_id = %s AND sb.player_id = %s
            """

        # Tuple containing the values for the WHERE clause
        values = (game_id, player_id)

        # Execute the update query with the provided values
        cur.execute(update_query, values)

        # Commit the changes to the database
        db_connection.commit()
        print("Total score updated successfully!")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

    finally:
        if db_connection:
            # Close the connection
            db_connection.close()


# Define a function to a dd a new player and check if it exists to the players table
def check_and_add_player(username, password):
    try:
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()

        # Check if the player exists
        query = "SELECT id, username FROM players WHERE username = %s and password = %s"
        cursor.execute(query, (username, password))
        existing_player = cursor.fetchone()

        if existing_player:
            # Player exists, return ID and username
            player_id, existing_username = existing_player
            print(f"Player {existing_username} with ID {player_id} already exists.")
            return {"player_id": player_id, "username": existing_username}
        else:
            # Player does not exist, add a new player
            insert_query = "INSERT INTO players (username, password) VALUES (%s, %s)"
            data = (username, password)
            cursor.execute(insert_query, data)
            db_connection.commit()

            new_player_id = cursor.lastrowid
            print(f"New player {username} added with ID {new_player_id}.")
            return {"player_id": new_player_id, "username": username}

    except Exception:
        raise DbConnectionError("Failed to insert data to DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


# def set_question(difficulty_level, question_text, correct_answer, incorrect_answer_1, incorrect_answer_2,
#                  incorrect_answer_3):
#     try:
#         db_name = "trivia_game"
#         db_connection = _connect_to_db(db_name)
#         cur = db_connection.cursor()
#         print(f"Connected to database {db_name}")
#
#         query = f"""
#                     INSERT INTO `trivia_game`.`questions` (`difficulty_level`, `question_text`, `correct_answer`,
#                         `incorrect_answer_1`, `incorrect_answer_2`, `incorrect_answer_3`)
#                     VALUES ('{difficulty_level}', '{question_text}', '{correct_answer}',
#                         '{incorrect_answer_1}', '{incorrect_answer_2}', '{incorrect_answer_3}')
#                 """
#
#         cur.execute(query)
#         db_connection.commit()
#         cur.close()
#
#     except mysql.connector.Error as err:
#         print(f"MySQL Error: {err}")
#
#     except Exception as exc:
#         print(f"An unexpected error occurred: {exc}")
#
#     finally:
#         if db_connection:
#             db_connection.close()


def main():
    # Run relevant functions below to ensure connecting to DB is successful:

    # Check player username exists:
    check_player_exists("helenvu")  # exists
    check_player_exists("hsfhsvsd")  # doesn't exist

    # Add a new player to players table:
    add_new_player("marshmallow-squisher")

    # Add a new game to DB when player starts game:
    add_new_game(2)

    # Add a new question to questions table including game_id and player_id as well:
    add_new_questions(2, 2, "easy", "What is the capital of France?",
                      "Paris", "Berlin", "London",
                      "Madrid")

    # Load questions into game_questions table at start of game, with player answer and is_correct set to None
    # p.s. None in Python is equal to NULL in mySQL
    start_game_questions(2, 2, 4, None, "Paris", None)

    # Load scoreboard at start of game and set player's score to zero
    start_game_scoreboard(2, 2, 0)

    # update game_questions with player_answer and evaluate whether is_correct at the same time
    game_id = 2  # Replace with the actual game_id
    player_id = 2  # Replace with the actual player_id
    question_id = 4  # Replace with the actual question_id
    player_answer = "Paris"  # Replace with the actual player's answer
    update_player_answer_is_correct(game_id, player_id, question_id, player_answer)

    # Update total_score in scoreboard after each question is answered:
    update_scoreboard_total_score(2, 2)


#     player_info = check_and_add_player('JohnDoe', 'password123')
#     print(player_info)


if __name__ == '__main__':
    main()
