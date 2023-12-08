import unittest
import json
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify
from werkzeug.test import Client
from app import app, User, Game


class TestAddGameRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.User.get_or_create')
    @patch('app.Game.start_game')
    @patch('app.Game.provide_question')
    def test_successful_game_creation(self, mock_provide_question, mock_start_game, mock_get_or_create):
        # Mocking specific methods of User and Game classes
        mock_get_or_create.return_value = 1  # Assuming user_id is 1
        mock_start_game.return_value = 1  # Assuming game_id is 1
        mock_provide_question.return_value = "test_question"  # Assuming a test question

        user_name = "helen"
        user_data = {"user_name": user_name}
        response = self.app.post('/add_new_game', json=user_data)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Manually create the expected JSON response
        expected_response = {
            "player_id": 1,
            "game_id": 1,
            "question": "test_question"
        }

        # Compare the expected response with the actual JSON content
        self.assertEqual(response.get_json(), expected_response)

        # Check that User and Game classes were called with the correct arguments
        mock_get_or_create.assert_called_once_with()
        mock_start_game.assert_called_once_with()
        mock_provide_question.assert_called_once_with(1)  # Assuming game_id is 1

    def test_failure_missing_user_name(self):
        response = self.app.post('/add_new_game', json={})

        # Check the response status code
        self.assertEqual(response.status_code, 400)  # Assuming a 400 Bad Request status code

    def test_failure_empty_user_name(self):
        user_data_empty = {"user_name": ""}
        response_empty = self.app.post('/add_new_game', json=user_data_empty)

        # Check the response status code
        self.assertEqual(response_empty.status_code, 400)  # Assuming a 400 Bad Request status code

    def test_failure_long_user_name(self):
        long_user_name = "b" * 41  # Assuming a username longer than 40 characters
        user_data_long = {"user_name": long_user_name}
        response_long = self.app.post('/add_new_game', json=user_data_long)
        data_long = response_long.json

        # Check the response status code and content
        self.assertEqual(response_long.status_code, 400)  # Assuming a 400 Bad Request status code
        self.assertIn('message', data_long)
        self.assertEqual(data_long['message'], 'User name must be between 1 and 40 characters')

    @patch('app.User')
    def test_failure_internal_server_error(self, mock_user):
        # Mocking only the User class
        mock_user_instance = MagicMock()
        mock_user_instance.get_or_create.side_effect = Exception("Simulated internal server error")
        mock_user.return_value = mock_user_instance

        user_name = "john"
        user_data = {"user_name": user_name}
        response_error = self.app.post('/add_new_game', json=user_data)

        # Check the response status code
        self.assertEqual(response_error.status_code, 500)  # Assuming a 500 Internal Server Error status code


class CheckAnswerTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()

    def test_check_answer_valid_input(self):
        # Mock the Game.check_answer method to return a known result
        with patch('app.Game.check_answer') as mock_check_answer:
            mock_check_answer.return_value = True

            # Make a request with valid input
            response = self.app.put('/check_answer', json={
                "game_id": "test_game",
                "answer": "test_answer",
                "question_id": "test_question"
            })

            # Check the response status code and content
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"result": True})

    def test_check_answer_missing_fields(self):
        # Make a request with missing fields
        response = self.app.put('/check_answer', json={
            "game_id": "test_game",
            "question_id": "test_question"
            # Missing the "answer" field
        })

        # Check the response status code and content
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Missing required fields"})

    def test_check_answer_invalid_content_type(self):
        # Make a request with an invalid content type
        response = self.app.put('/check_answer', data={
            "game_id": "test_game",
            "answer": "test_answer",
            "question_id": "test_question"
        })

        # Check the response status code and content
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"message": "Invalid content type. Expected JSON"})

    def test_check_answer_internal_server_error(self):
        # Mock the Game.check_answer method to raise an exception
        with patch('app.Game.check_answer') as mock_check_answer:
            mock_check_answer.side_effect = Exception("Simulated internal server error")

            # Make a request with valid input
            response = self.app.put('/check_answer', json={
                "game_id": "test_game",
                "answer": "test_answer",
                "question_id": "test_question"
            })

            # Check the response status code and content
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json, {"message": "Internal server error"})


class TestNextQuestionRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_next_question_route(self):
        game_id = 1
        response = self.app.get(f'/next_question/{game_id}')
        if response.status_code == 200:
            self.assertIn('question', response.get_data(as_text=True))
        else:
            self.assertEqual(response.status_code, 404)


class TestLeaderboardRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_leaderboard_route(self):
        response = self.app.get('/leaderboard/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()



# class TestCheckAnswerRoute(unittest.TestCase):
#
#     def setUp(self):
#         self.app = app.test_client()
#
#     def test_check_answer_route(self):
#         answer_data = {
#             "game_id": 1,
#             "answer": "The Bahamas Archipelago",
#             "question_id": 46
#         }
#         response = self.app.put('/check_answer', json=answer_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('score', response.get_data(as_text=True))
#         self.assertIn('correct_answer', response.get_data(as_text=True))
#         self.assertIn('result', response.get_data(as_text=True))

