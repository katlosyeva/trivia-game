import unittest
from unittest.mock import MagicMock, patch
from db_utils import (
    get_or_add_player_id,
    add_new_game,
    add_new_questions,
    display_question_to_player,
    update_game_score,
    get_user_score,
    get_leaderboard
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
        self.assertEqual(new_result,2)  # Assuming the new player gets player_id (doesn't work as expected as test
        # return random virtual ID)

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
        user_id = 3  # Assuming user_id 1 (replace as needed)
        score = 15  # Assuming a score of 100 (replace as needed)
        game_id = add_new_game(user_id, score)

        # Assertions:
        # Check that the result is as expected
        self.assertEqual(game_id, 17)  # Assuming the last inserted row ID is 17

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that execute() was called on the mock_cursor to insert a new game
        insert_query = "INSERT INTO games (user_id, score) VALUES (%s, %s)"
        expected_values = (user_id, score)
        mock_cursor.execute.assert_called_once_with(insert_query, expected_values)


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
                    is_provided
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        expected_values = (game_id, question_text, correct_answer, incorrect_answers[0], incorrect_answers[1],
                           incorrect_answers[2], False)
        mock_cursor.execute.assert_called_once_with(expected_query, expected_values)

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
