import mysql.connector  # module that allows to establish database connection
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


# Function which checks whether username exists and returns player_id,
# and if username does not exist, new username is added to players and returns new player_id:


def get_or_add_player_id(username):
    player_id = None

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


# DB function to add new game to DB
def add_new_game(user_id, score=0):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query for inserting a new row into the 'games' table
        insert_query = "INSERT INTO games (user_id, score) VALUES (%s, %s)"
        # values to be inserted
        data = (user_id, score)
        # Execute the query with the provided values
        cur.execute(insert_query, data)
        # Commit the changes to the database
        db_connection.commit()
        print("Game successfully added to DB!")

        # Get the ID of the last inserted row (game_id)
        game_id = cur.lastrowid
        print(f"add_new_game function returns game_id: {game_id}\n")

        # Close the cursor
        cur.close()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}\n")
        game_id = None  # Set game_id to None in case of an error

    except Exception as exc:
        print(f"An unexpected error occurred: {exc}\n")
        game_id = None  # Set game_id to None in case of an error

    finally:
        if db_connection:
            # close the connection
            db_connection.close()

    return game_id


# DB function to add questions data to questions table in DB - will be used for API call
def add_new_questions(game_id, question_text, correct_answer, incorrect_answers):
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
                    is_provided
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

        # Tuple containing the values to be inserted
        values = (game_id,
                  question_text,
                  correct_answer,
                  incorrect_answers[0],
                  incorrect_answers[1],
                  incorrect_answers[2],
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
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the question details
        query = f"""
                SELECT id, game_id, question, correct_answer, answer_1, answer_2, answer_3
                FROM questions
                WHERE game_id = {game_id}
                AND is_provided = False
                LIMIT 1
            """

        cur.execute(query)
        question_displayed = cur.fetchone()
        query2 = f"""
                UPDATE questions
                SET is_provided = True
                WHERE id = {question_displayed[0]}
                """
        cur.execute(query2)
        db_connection.commit()
        cur.close()
        # Return the individual variables
        # if question_displayed:
        question_id = question_displayed[0]
        game_id = question_displayed[1]
        question_text = question_displayed[2]
        answers = [question_displayed[3], question_displayed[4], question_displayed[5], question_displayed[6]]
        answers.sort()

        return {
            "question_id": question_id,
            "game_id": game_id,
            "question_text": question_text,
            "answers": answers
        }


    except Exception:
        return {"error": "No more questions"}

    finally:
        if db_connection:
            db_connection.close()


def display_question_to_player_fifty_fifty(question_id):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the question details
        query = f"""
                SELECT id, game_id, question, correct_answer, answer_1
                FROM questions
                WHERE id = {question_id}
            """

        cur.execute(query)
        question_displayed = cur.fetchone()

        db_connection.commit()
        cur.close()

        # if question_displayed:
        question_id = question_displayed[0]
        game_id = question_displayed[1]
        question_text = question_displayed[2]
        answers = [question_displayed[3], question_displayed[4]]
        answers.sort()

        return {
            "question_id": question_id,
            "game_id": game_id,
            "question_text": question_text,
            "answers": answers
        }

    except Exception as exc:
        return {"error": exc}

    finally:
        if db_connection:
            db_connection.close()


def get_correct_answer(question_id):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the question details
        query = f"""
                    SELECT correct_answer
                    FROM questions
                    WHERE id = {question_id}
                """

        cur.execute(query)
        correct_answer = cur.fetchone()
        cur.close()

        return correct_answer[0]


    except Exception:
        raise DbConnectionError("Failed to fetch question from DB\n")

    finally:
        if db_connection:
            db_connection.close()


def update_game_score(game_id):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        query1 = f"""
                UPDATE games
                SET score = score + 1
                WHERE id = {game_id}
            """
        cur.execute(query1)
        db_connection.commit()
        query2 = f"""
               SELECT score
               FROM games
               WHERE id = {game_id}
            """
        cur.execute(query2)
        player_score = cur.fetchone()
        cur.close()

        return player_score[0]
    except Exception:
        raise DbConnectionError("Failed to update and fetch update score\n")

    finally:
        if db_connection:
            # Close the connection
            db_connection.close()


def get_user_score(game_id):
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()  # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the score details
        query = f"""
                    SELECT score
                    FROM games
                    WHERE id = {game_id}
                """

        cur.execute(query)
        score = cur.fetchone()
        cur.close()

        return score[0]

    except Exception:
        raise DbConnectionError("Failed to fetch score from DB\n")

    finally:
        if db_connection:
            db_connection.close()



def get_leaderboard():
    try:
        # Establish a connection to the MySQL database
        db_name = "trivia_game"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor() # Create a cursor object to interact with the database
        print(f"Connected to database {db_name}")

        # SQL query to fetch the score details
        query = f"""
                    SELECT players.username, games.score
                    FROM players
                    JOIN games ON players.id = games.user_id
                    ORDER BY games.score DESC
                """

        cur.execute(query)
        leaderboard = cur.fetchall()
        cur.close()

        return leaderboard[:10]

    except Exception:
        raise DbConnectionError("Failed to retrieve leaderboard from DB\n")

    finally:
        if db_connection:
            db_connection.close()



def main():
    pass
    # print(add_new_game(1))
    # print(display_question_to_player(1))
    # add_new_questions(1, "Blablabla", "gla", ["na", "ma", "pa"])
    # print(update_game_score(24))
    # print(get_correct_answer(13))
    # get_or_add_player_id("Megan")
    # add_new_questions(2, "HHHH", "HE", ["TU", "TT","hhh"])
    # print(get_leaderboard())


if __name__ == '__main__':
    main()
