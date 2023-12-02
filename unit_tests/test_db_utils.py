import unittest
from unittest.mock import MagicMock, patch

from db_utils import (
    get_or_add_player_id,
    add_new_game,
    add_new_questions,
    display_question_to_player,
    display_question_to_player_fifty_fifty,
    get_correct_answer,
    update_game_score,
    get_user_score,
    get_leaderboard,
    DbConnectionError
)


class TestGetOrAddPlayerId(unittest.TestCase):
    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_existing_player(self, mock_connect):
        # Set up the mock behavior
        mock_connection = MagicMock()  # for database interactions, use mocking to replace actual database calls with
        # mock objects
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        mock_cursor.fetchone.return_value = (1,)

        # Test with the mocked database connection for an existing player
        existing_username = 'helenvu'
        existing_result = get_or_add_player_id(existing_username)

        # Check that the result is as expected
        self.assertEqual(existing_result, 1)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_add_new_player(self, mock_connect):
        mock_connection_new = MagicMock()
        mock_cursor_new = MagicMock()
        mock_cursor_new.fetchone.return_value = None  # Simulate that the player doesn't exist
        mock_cursor_new.lastrowid = 2  # Set lastrowid for the new player
        mock_connection_new.cursor.return_value = mock_cursor_new
        mock_connect.return_value = mock_connection_neweturn_value = mock_connection_new

        # Test with the mocked database connection
        new_username = 'paul'
        new_result = get_or_add_player_id(new_username)

        #  Check that the result is as expected
        self.assertEqual(new_result, 2)  # Assuming the new player gets player_id (doesn't work as expected as test
        # return random virtual ID)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_invalid_empty_username(self, mock_connect):
        # Set up the mock behavior for an invalid case
        mock_connection_invalid = MagicMock()
        mock_cursor_invalid = MagicMock()
        mock_cursor_invalid.fetchone.return_value = None  # Simulate that the player doesn't exist
        mock_cursor_invalid.lastrowid = -1  # Set lastrowid for the invalid case
        mock_connection_invalid.cursor.return_value = mock_cursor_invalid
        mock_connect.return_value = mock_connection_invalid

        # Test with the mocked database connection for an invalid case
        invalid_username = ''  # Invalid username (empty string)
        invalid_result = get_or_add_player_id(invalid_username)

        # Check that the result is as expected (e.g., -1 or any indicator for an invalid case)
        self.assertEqual(invalid_result, -1)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_exceeds_username_limit(self, mock_connect):
        # Set up the mock behavior for the case where the username exceeds the limit
        mock_connection_invalid = MagicMock()
        mock_cursor_invalid = MagicMock()
        mock_cursor_invalid.fetchone.return_value = None  # Simulate that the player doesn't exist
        mock_cursor_invalid.lastrowid = -1  # Set lastrowid for the invalid case
        mock_connection_invalid.cursor.return_value = mock_cursor_invalid
        mock_connect.return_value = mock_connection_invalid

        # Test with the mocked database connection for the case where the username exceeds the limit
        invalid_username = 'a' * 41  # Username with 41 characters, exceeding the 40-character limit
        invalid_result = get_or_add_player_id(invalid_username)

        # Check that the result is as expected (e.g., -1 or any indicator for an invalid case)
        self.assertEqual(invalid_result, -1)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')


class TestAddNewGame(unittest.TestCase):

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_add_new_game(self, mock_connect):
        # Set up the mock behavior
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 17  # Mock the last inserted row ID
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection
        user_id = 3  # Assuming user_id 1
        game_id = add_new_game(user_id)

        # Assertions:
        # Check that the result is as expected
        self.assertEqual(game_id, 17)  # Assuming the last inserted row ID is 17

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that execute() was called on the mock_cursor to insert a new game
        insert_query = "INSERT INTO games (user_id, score) VALUES (%s, 0)"
        expected_values = (user_id,)
        mock_cursor.execute.assert_called_once_with(insert_query, expected_values)

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_database_error(self, mock_connect):
        # Set up the mock behavior for a database error
        mock_connect.side_effect = Exception('Database error')  # Simulate a database error

        # Test with the mocked database connection for a database error
        user_id = 4
        game_id = add_new_game(user_id)

        # Assertions:
        # Check that the result is None for a database error
        self.assertIsNone(game_id)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_connection_error(self, mock_connect):
        # Set up the mock behavior for a connection error
        mock_connect.side_effect = Exception('Connection error')  # Simulate a connection error

        # Test with the mocked database connection for a connection error
        user_id = 5
        game_id = add_new_game(user_id)

        # Assertions:
        # Check that the result is None for a connection error
        self.assertIsNone(game_id)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_add_new_game_negative_user_id(self, mock_connect):
        # Set up the mock behavior
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection and a user_id that is a negative integer
        user_id = -42
        game_id = add_new_game(user_id)

        # Assertions:
        if game_id is not None:
            # Check that the result is a positive integer (assuming positive game_id is expected)
            self.assertGreater(game_id, 0)
            # Check that _connect_to_db was called with the correct arguments
            mock_connect.assert_called_with('trivia_game')
            # Check that execute() was called on the mock_cursor due to the invalid user_id
            mock_cursor.execute.assert_called_once_with('INSERT INTO games (user_id, score) VALUES (%s, 0)', (user_id,))
        else:
            # Ensure that _connect_to_db was not called when user_id is invalid
            mock_connect.assert_not_called()
            # Ensure that execute() was not called when add_new_game returns None
            mock_cursor.execute.assert_not_called()


class TestAddNewQuestions(unittest.TestCase):

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_add_new_questions(self, mock_connect):
        # Mocking the database connection and cursor
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mocking the execute method to avoid actual database operations
        mock_cursor.execute.return_value = None

        # Input values for the function
        game_id = 1
        question_text = "What is the capital of France?"
        correct_answer = "Paris"
        incorrect_answers = ["Berlin", "Madrid", "Rome"]

        # Call the function
        add_new_questions(game_id, question_text, correct_answer, incorrect_answers)

        # Assertions
        mock_connect.assert_called_once_with('trivia_game')  # Assuming 'trivia_game' is the expected database name
        mock_connection.cursor.assert_called_once()

        expected_query = """
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
        expected_values = (game_id, question_text, correct_answer, incorrect_answers[0], incorrect_answers[1],
                           incorrect_answers[2], False)
        mock_cursor.execute.assert_called_once_with(expected_query, expected_values)

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_add_new_questions_unexpected_error(self, mock_connect):
        # Mocking the database connection and cursor
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mocking an unexpected error
        mock_cursor.execute.side_effect = Exception("Test unexpected error")

        # Input values for the function
        game_id = 1
        question_text = "What is the capital of France?"
        correct_answer = "Paris"
        incorrect_answers = ["Berlin", "Madrid", "Rome"]

        try:
            # Call the function
            add_new_questions(game_id, question_text, correct_answer, incorrect_answers)
        except Exception as e:
            print(f"Caught exception: {e}")

        # Assertions
        mock_connect.assert_called_once_with('trivia_game')  # Assuming 'trivia_game' is the expected database name
        mock_connection.cursor.assert_called_once()

        expected_query = """
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
        expected_values = (game_id, question_text, correct_answer, incorrect_answers[0], incorrect_answers[1],
                           incorrect_answers[2], False)
        mock_cursor.execute.assert_called_once_with(expected_query, expected_values)


class TestDisplayQuestionToPlayer(unittest.TestCase):

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_display_question_to_player(self, mock_connect):
        # Mocking the database connection and cursor
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mocking the execute method to avoid actual database operations
        mock_cursor.execute.return_value = None

        # Mocking the fetchone method to simulate a question being returned
        mock_cursor.fetchone.return_value = (
            1, 1, "What is the capital of France?", "Paris", "Berlin", "Madrid", "Rome"
        )

        # Input values for the function
        game_id = 1

        # Mocking random.sample to ensure predictable shuffling for testing
        with patch('random.sample', side_effect=lambda data, k: data[:k]):
            # Call the function
            result = display_question_to_player(game_id)

        # Assertions
        mock_connect.assert_called_once_with('trivia_game')  # Assuming 'trivia_game' is the expected database name
        mock_connection.cursor.assert_called_once()

        # Check the first execute call for the SELECT query
        expected_query_select = """
            SELECT id, game_id, question, correct_answer, answer_1, answer_2, answer_3
            FROM questions
            WHERE game_id = %s
            AND already_displayed = False
            LIMIT 1
        """
        expected_values_select = (game_id,)
        mock_cursor.execute.assert_any_call(expected_query_select, expected_values_select)

        # Check the second execute call for the UPDATE query
        expected_query_update = """
                UPDATE questions
                SET already_displayed = True
                WHERE id = %s
            """
        expected_values_update = (1,)  # Assuming the question_id is always 1 for this test
        mock_cursor.execute.assert_any_call(expected_query_update, expected_values_update)

        # Additional assertions
        mock_cursor.fetchone.assert_called_once()

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

        # Additional assertions for the returned result with shuffled answers
        expected_result = {
            "question_id": 1,
            "game_id": 1,
            "question_text": "What is the capital of France?",
            "answers": ["Berlin", "Madrid", "Paris", "Rome"]  # Adjusted to the shuffled order
        }
        self.assertEqual(result["question_id"], expected_result["question_id"])
        self.assertEqual(result["game_id"], expected_result["game_id"])
        self.assertEqual(result["question_text"], expected_result["question_text"])

        # Use assertCountEqual to check if the answers are the same regardless of order
        self.assertCountEqual(result["answers"], expected_result["answers"])

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_no_more_questions(self, mock_connect):
        # Mocking the database connection and cursor for the case where there are no more questions
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mocking the execute method to simulate no more questions being returned
        mock_cursor.fetchone.return_value = None

        # Input values for the function
        game_id = 1

        # Call the function
        result = display_question_to_player(game_id)

        # Assertions for the case where there are no more questions
        mock_connect.assert_called_once_with('trivia_game')  # Assuming 'trivia_game' is the expected database name
        mock_connection.cursor.assert_called_once()

        # Check the execute call for the SELECT query
        expected_query_select = """
            SELECT id, game_id, question, correct_answer, answer_1, answer_2, answer_3
            FROM questions
            WHERE game_id = %s
            AND already_displayed = False
            LIMIT 1
        """
        expected_values_select = (game_id,)
        mock_cursor.execute.assert_called_once_with(expected_query_select, expected_values_select)

        # Additional assertions for the returned result when there are no more questions
        expected_result = {"error": "No more questions"}
        self.assertEqual(result, expected_result)

        # Additional assertions for no further interactions with the cursor and connection
        mock_cursor.fetchone.assert_called_once()
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_shuffling_order(self, mock_connect):
        # Mocking the database connection and cursor
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mocking the execute method to avoid actual database operations
        mock_cursor.execute.return_value = None

        # Mocking the fetchone method to simulate a question being returned
        mock_cursor.fetchone.return_value = (
            1, 1, "What is the capital of France?", "Paris", "Berlin", "Madrid", "Rome"
        )

        # Input values for the function
        game_id = 1

        # Call the function
        result = display_question_to_player(game_id)

        # Assertions
        mock_connect.assert_called_once()  # Assuming 'trivia_game' is the expected database name
        mock_connection.cursor.assert_called_once()

        # Check the execute call for the SELECT query
        expected_query_select = """
            SELECT id, game_id, question, correct_answer, answer_1, answer_2, answer_3
            FROM questions
            WHERE game_id = %s
            AND already_displayed = False
            LIMIT 1
        """
        expected_values_select = (game_id,)
        mock_cursor.execute.assert_any_call(expected_query_select, expected_values_select)

        # Check the execute call for the UPDATE query
        expected_query_update = """
                UPDATE questions
                SET already_displayed = True
                WHERE id = %s
            """
        expected_values_update = (1,)  # Assuming the question_id is always 1 for this test
        mock_cursor.execute.assert_any_call(expected_query_update, expected_values_update)

        # Additional assertions
        mock_cursor.fetchone.assert_called_once()

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

        # Additional assertions for the returned result with shuffled answers
        expected_result = {
            "question_id": 1,
            "game_id": 1,
            "question_text": "What is the capital of France?",
            "answers": ["Berlin", "Madrid", "Paris", "Rome"]  # Adjusted to the shuffled order
        }
        self.assertEqual(result["question_id"], expected_result["question_id"])
        self.assertEqual(result["game_id"], expected_result["game_id"])
        self.assertEqual(result["question_text"], expected_result["question_text"])

        # Use assertCountEqual to check if the answers are the same regardless of order
        self.assertCountEqual(result["answers"], expected_result["answers"])


class TestDisplayQuestionToPlayerFiftyFifty(unittest.TestCase):

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_display_question_to_player_fifty_fifty(self, mock_connect):
        # Set up the mock behavior
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection and a question_id
        question_id = 42
        correct_answer = "Paris"
        incorrect_answer = "Berlin"

        mock_cursor.fetchone.return_value = (1, 1, f"What is the capital of France?", correct_answer, incorrect_answer)

        # Call the function
        result = display_question_to_player_fifty_fifty(question_id)

        # Assertions:
        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Check that the expected keys are present in the result
        expected_keys = ["question_id", "game_id", "question_text", "answers"]
        self.assertCountEqual(result.keys(), expected_keys)

        # Check that the correct keys have the expected values
        self.assertEqual(result["question_id"], 1)
        self.assertEqual(result["game_id"], 1)
        self.assertEqual(result["question_text"], f"What is the capital of France?")

        # Check that the answers list has two elements
        self.assertEqual(len(result["answers"]), 2)

        # Check that the database connection was closed
        mock_connection.close.assert_called_once()

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_edge_case_empty_result(self, mock_connect):
        # Set up the mock behavior for an empty result (edge case)
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None  # Simulate an empty result
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection and an existing question_id
        existing_question_id = 42
        result = display_question_to_player_fifty_fifty(existing_question_id)

        # Assertions:
        # Check if result is a dictionary
        self.assertIsInstance(result, dict)

        if 'error' in result:
            # Check that the error message is as expected
            expected_error_message = f"Question with ID {existing_question_id} not found."
            self.assertEqual(str(result.get('error', '')), expected_error_message)
        else:
            # Check that the keys are present in the result dictionary
            expected_keys = ["question_id", "game_id", "question_text", "answers"]
            for key in expected_keys:
                self.assertIn(key, result)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that execute() was called on the mock_cursor with the correct query
        expected_query = """
                SELECT id, game_id, question, correct_answer, answer_1
                FROM questions
                WHERE id = %s
            """
        mock_cursor.execute.assert_called_once_with(expected_query, (existing_question_id,))

        # Check additional assertions
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()  # Add this line
        mock_connection.close.assert_called_once()

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_existing_question_id(self, mock_connect):
        # Set up the mock behavior
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, 2, 'Sample Question', 'Correct Answer', 'Incorrect Answer')
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection and an existing question_id
        question_id = 1
        result = display_question_to_player_fifty_fifty(question_id)

        # Assertions:
        self.assertIsNotNone(result)
        self.assertIn('question_id', result)
        self.assertIn('game_id', result)
        self.assertIn('question_text', result)
        self.assertIn('answers', result)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that execute() was called on the mock_cursor with the correct query and values
        expected_query = """
                SELECT id, game_id, question, correct_answer, answer_1
                FROM questions
                WHERE id = %s
            """
        expected_values = (question_id,)
        mock_cursor.execute.assert_called_once_with(expected_query, expected_values)

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_non_existent_question_id(self, mock_connect):
        # Set up the mock behavior for a non-existent question_id
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None  # Simulate non-existent question
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection and a non-existent question_id
        question_id = 9999
        result = display_question_to_player_fifty_fifty(question_id)

        # Assertions:
        self.assertIsNotNone(result)
        self.assertIn('error', result)
        expected_error_message = f"Question with ID {question_id} not found."
        self.assertEqual(result['error'], expected_error_message)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that execute() was called on the mock_cursor with the correct query and values
        expected_query = (
            """
                SELECT id, game_id, question, correct_answer, answer_1
                FROM questions
                WHERE id = %s
            """
        )
        expected_values = (question_id,)
        mock_cursor.execute.assert_called_once_with(expected_query, expected_values)


class TestGetCorrectAnswer(unittest.TestCase):

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_successful_fetch(self, mock_connect):
        # Set up the mock behavior
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection and a question_id
        question_id = 42
        correct_answer = "Paris"
        mock_cursor.fetchone.return_value = (correct_answer,)

        # Call the function
        result = get_correct_answer(question_id)

        # Assertions:
        # Check that the result is the correct answer
        self.assertEqual(result, correct_answer)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that execute() was called on the mock_cursor with the correct query and values
        expected_query = """
                        SELECT correct_answer
                        FROM questions
                        WHERE id = %s
                        """
        expected_values = (question_id,)
        mock_cursor.execute.assert_called_once_with(expected_query, expected_values)

        # Check additional assertions
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_no_question_found(self, mock_connect):
        # Set up the mock behavior for no question found
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None  # Simulate no question found
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection and a question_id
        non_existing_question_id = 9999

        with self.assertRaises(ValueError) as context:
            # Call the function
            get_correct_answer(non_existing_question_id)

        # Assertions:
        # Check that the correct ValueError is raised
        expected_error_message = f"No question found with ID {non_existing_question_id}"
        self.assertEqual(str(context.exception), expected_error_message)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that execute() was called on the mock_cursor with the correct query and values
        expected_query = """
                        SELECT correct_answer
                        FROM questions
                        WHERE id = %s
                        """
        expected_values = (non_existing_question_id,)
        mock_cursor.execute.assert_called_once_with(expected_query, expected_values)

        # Check additional assertions
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_db_connection_error(self, mock_connect):
        # Set up the mock behavior for a database connection error
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        def execute_side_effect(query, values):
            raise Exception('Database connection error')

        mock_cursor.execute.side_effect = execute_side_effect
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection and a question_id
        question_id = 42

        with self.assertRaises(DbConnectionError) as context:
            # Call the function
            get_correct_answer(question_id)

        # Assertions:
        # Check that the correct DbConnectionError is raised
        expected_error_message = "Failed to fetch question from DB"
        self.assertEqual(str(context.exception), expected_error_message)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check additional assertions
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            """
                        SELECT correct_answer
                        FROM questions
                        WHERE id = %s
                        """, (question_id,)
        )
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()


class TestUpdateGameScore(unittest.TestCase):

    @patch('db_utils._connect_to_db')
    def test_update_game_score_success(self, mock_connect_to_db):
        # Mock the database connection
        mock_db_connection = mock_connect_to_db.return_value
        mock_cursor = mock_db_connection.cursor.return_value

        # Set up a mock game_id
        game_id = 123

        # Call the function
        update_game_score(game_id)

        # Check if the correct SQL query was executed
        expected_query = """
            UPDATE games
            SET score = score + 1
            WHERE id = %s
        """
        mock_cursor.execute.assert_called_once_with(expected_query, (game_id,))
        mock_db_connection.commit.assert_called_once()

        # Check if the cursor and connection were closed
        mock_cursor.close.assert_called_once()
        mock_db_connection.close.assert_called_once()

    @patch("db_utils._connect_to_db")
    def test_update_game_score_invalid_game_id(self, mock_connect_to_db):
        # Set up an invalid mock game_id (non-integer)
        invalid_game_id = "invalid_id"

        # Call the function and check for the expected exception
        with self.assertRaises(ValueError) as context:
            update_game_score(invalid_game_id)

        # Ensure the exception type is ValueError
        self.assertEqual(ValueError, type(context.exception))

        # Ensure the exception message contains the expected string
        expected_error_message = "Invalid game_id. Please provide an integer."
        self.assertIn(expected_error_message, str(context.exception))

    @patch('db_utils._connect_to_db')
    def test_update_game_score_db_error(self, mock_connect_to_db):
        # Mock the database connection to raise an exception
        mock_db_connection = mock_connect_to_db.return_value
        mock_db_connection.cursor.side_effect = Exception("Database error")

        # Set up a mock game_id
        game_id = 123

        # Call the function and check for the expected exception
        with self.assertRaises(DbConnectionError) as context:
            update_game_score(game_id)

        expected_error_message = "Failed to update game score in DB"
        self.assertEqual(str(context.exception), expected_error_message)

        # Check if the cursor and connection were closed even in case of an error
        mock_db_connection.cursor.assert_called_once()
        mock_db_connection.close.assert_called_once()


class TestGetUserScore(unittest.TestCase):
    @patch("db_utils._connect_to_db")
    def test_get_user_score_success(self, mock_connect_to_db):
        # Mocking the database connection and cursor
        mock_db_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect_to_db.return_value = mock_db_connection
        mock_db_connection.cursor.return_value = mock_cursor

        # Mocking the execute result
        mock_cursor.fetchone.return_value = (42,)

        # Call the function
        result = get_user_score(game_id=123)

        # Assertions
        self.assertEqual(result, 42)
        mock_connect_to_db.assert_called_once_with("trivia_game")
        mock_db_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db_connection.close.assert_called_once()

    @patch("db_utils._connect_to_db")
    def test_get_user_score_db_error(self, mock_connect_to_db):
        # Mocking the database connection and cursor
        mock_db_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect_to_db.return_value = mock_db_connection
        mock_db_connection.cursor.return_value = mock_cursor

        # Mocking an exception during execution
        mock_cursor.execute.side_effect = Exception("Database error")

        # Call the function
        with self.assertRaises(DbConnectionError) as context:
            get_user_score(game_id=123)

        # Assertions
        self.assertEqual(
            str(context.exception), "Failed to fetch score from DB\n"
        )
        mock_connect_to_db.assert_called_once_with("trivia_game")
        mock_db_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db_connection.close.assert_called_once()

    @patch("db_utils._connect_to_db")
    def test_get_user_score_no_data(self, mock_connect_to_db):
        # Mocking the database connection and cursor
        mock_db_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect_to_db.return_value = mock_db_connection
        mock_db_connection.cursor.return_value = mock_cursor

        # Mocking the case where no data is found
        mock_cursor.fetchone.return_value = None

        # Call the function
        with self.assertRaises(DbConnectionError) as context:
            get_user_score(game_id=999)

        # Assertions
        self.assertEqual(
            str(context.exception), "Failed to fetch score from DB\n"
        )
        mock_connect_to_db.assert_called_once_with("trivia_game")
        mock_db_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db_connection.close.assert_called_once()


class TestGetLeaderboard(unittest.TestCase):

    @patch('db_utils._connect_to_db')
    def test_get_leaderboard_success(self, mock_connect_to_db):
        # Mock the database connection
        mock_db_connection = mock_connect_to_db.return_value
        mock_cursor = mock_db_connection.cursor.return_value

        # Set up a mock leaderboard data
        mock_leaderboard_data = [
            ('user1', 100),
            ('user2', 90),
            ('user3', 80),
            ('user4', 70),
            ('user5', 60)
        ]

        mock_cursor.fetchall.return_value = mock_leaderboard_data

        # Call the function
        leaderboard = get_leaderboard()

        # Check if the correct SQL query was executed
        expected_query = """
            SELECT players.username, games.score
            FROM players
            JOIN games ON players.id = games.user_id
            ORDER BY games.score DESC
        """
        mock_cursor.execute.assert_called_once_with(expected_query)

        # Check if the result matches the expected leaderboard data
        self.assertEqual(leaderboard, mock_leaderboard_data)

        # Check if the cursor and connection were closed
        mock_cursor.close.assert_called_once()
        mock_db_connection.close.assert_called_once()

    @patch('db_utils._connect_to_db')
    def test_get_leaderboard_db_error(self, mock_connect_to_db):
        # Mock the database connection to raise an exception
        mock_db_connection = mock_connect_to_db.return_value
        mock_db_connection.cursor.side_effect = Exception("Database error")

        # Call the function and check for the expected exception
        with self.assertRaises(DbConnectionError) as context:
            get_leaderboard()

        expected_error_message = "Failed to retrieve leaderboard from DB"
        self.assertEqual(str(context.exception), expected_error_message)

        # Check if the cursor and connection were closed even in case of an error
        mock_db_connection.cursor.assert_called_once()
        mock_db_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
