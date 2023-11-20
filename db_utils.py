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



def set_question(difficulty_level, question_text, correct_answer, incorrect_answer_1, incorrect_answer_2,
                 incorrect_answer_3):
    try:
        db_name = 'trivia_game'
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
def add_question(difficulty_level, question_text, answer, is_correct):
    try:
        # Establish a connection to the 'trivia_game' database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f"Connected to database: {db_name}")

        query = "INSERT INTO questions (difficulty_level, question_text, answer, is_correct) VALUES (%s, %s, %s, %s)"
        data = (difficulty_level, question_text, answer, is_correct)
        cursor.execute(query, data)
        db_connection.commit()

        # Get the last inserted ID
        question_id = cursor.lastrowid

        cursor.close()

    except Exception:
        raise DbConnectionError("Failed to insert data to DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return {"question_id": question_id}


# def main():
#     # add new player
#     player_info = check_and_add_player('JohnDoe', 'password123')
#     print(player_info)




# if __name__ == '__main__':
    # main()
