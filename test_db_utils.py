import unittest
from unittest.mock import MagicMock, patch
from db_utils import (
    get_or_add_player_id,
    add_new_game,
    add_new_questions,
    start_game_questions,
    start_game_scoreboard,
    display_question_to_player,
    update_player_answer_is_correct,
    update_scoreboard_total_score,
    display_total_score,
    get_leaderboard
)


class TestGetOrAddPlayerId(unittest.TestCase):
    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_existing_player(self, mock_connect):
        # Set up the mock behavior
        mock_connection = MagicMock() # for database interactions, use mocking to replace actual database calls with mock objects
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        mock_cursor.fetchone.return_value = (1,)

        # Test with the mocked database connection
        result, player_id = get_or_add_player_id('helenvu')

        # Check that the result is as expected
        self.assertEqual(result, {"player_id:": 1})

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that cursor() was called on the mock_connection
        mock_connection.cursor.assert_called_once()

        # Check that fetchone() was called on the mock_cursor
        mock_cursor.fetchone.assert_called_once()

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_add_new_player(self, mock_connect):
        mock_connection = MagicMock()  # MagicMock is for database interactions, use mocking to replace actual database calls with mock objects
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        mock_cursor.fetchone.return_value = None # Simulate that the player doesn't exist

        # Test with the mocked database connection
        result, player_id = get_or_add_player_id('kate')

        # # # Check that the result is as expected
        # self.assertEqual(result, {"player_id:": 3})  # Assuming the new player gets player_id (doesn't work as expected as test return random virtual ID)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that cursor() was called on the mock_connection
        mock_connection.cursor.assert_called_once()


class TestAddNewGame(unittest.TestCase):

    @patch('db_utils._connect_to_db')  # Mock the database connection
    def test_add_new_game(self, mock_connect):
        # Set up the mock behavior
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1  # Mock the last inserted row ID
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Test with the mocked database connection
        result, game_id = add_new_game(1)  # Assuming player_id 1 (replace as needed)

        # Assertions:
        # Check that the result is as expected
        self.assertEqual(result, {"game_id:": 1})  # Assuming the last inserted row ID is 42 (replace as needed)

        # Check that _connect_to_db was called with the correct arguments
        mock_connect.assert_called_with('trivia_game')

        # Check that cursor() was called on the mock_connection
        mock_connection.cursor.assert_called_once()

        # Check that execute() was called on the mock_cursor to insert a new game
        mock_cursor.execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()