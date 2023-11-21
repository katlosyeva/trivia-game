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


def insert_into_questions(game_id, player_id, difficulty_level, question_text, correct_answer, incorrect_answer_1,
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
        print("Questions row inserted successfully!")

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


def set_question(difficulty_level, question_text, correct_answer, incorrect_answer_1, incorrect_answer_2,
                 incorrect_answer_3):
    try:
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to database {db_name}")

        query = f"""
                    INSERT INTO `trivia_game`.`questions` (`difficulty_level`, `question_text`, `correct_answer`,
                        `incorrect_answer_1`, `incorrect_answer_2`, `incorrect_answer_3`)
                    VALUES ('{difficulty_level}', '{question_text}', '{correct_answer}',
                        '{incorrect_answer_1}', '{incorrect_answer_2}', '{incorrect_answer_3}')
                """

        cur.execute(query)
        db_connection.commit()
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

    finally:
        if db_connection:
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


# Define a function to a dd a new game to the games table
def add_new_game(player_id, question_id, player_answer, correct_answer, is_correct):
    try:
        # Establish a connection to the 'trivia_game' database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f"Connected to database: {db_name}")

        query = "INSERT INTO games (player_id, question_id, player_answer, correct_answer, is_correct) VALUES (%s, %s, %s, %s, %s)"
        data = (player_id, question_id, player_answer, correct_answer, is_correct)
        cursor.execute(query, data)
        db_connection.commit()

        # Fetch the last inserted ID using LAST_INSERT_ID()
        cursor.execute("SELECT LAST_INSERT_ID()")
        game_id = cursor.fetchone()[0]

        cursor.close()

    except Exception:
        raise DbConnectionError("Failed to insert data to DB")


    finally:
        if db_connection:
            db_connection.close()

            print("DB connection is closed")

    return {"game_id": game_id}


# Define a function to a dd a new question to the questions table

def main():
    # Run relevant functions below to ensure connecting to DB is successful:

    # Add a new player to players table:
    add_new_player("marshmallow-squisher")

    # Add a new question to questions table including game_id and player_id as well:
    insert_into_questions(1, 1, "easy", "What is the capital of France?",
                          "Paris", "Berlin", "London",
                          "Madrid")


#     # add new player
#     player_info = check_and_add_player('JohnDoe', 'password123')
#     print(player_info)


if __name__ == '__main__':
    main()
