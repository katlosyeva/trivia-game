import unittest
from unittest.mock import MagicMock, patch
from app import app


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

    @patch('app.Game.provide_question')
    def test_next_question_game_ongoing(self, mock_provide_question):
        # Mocking the Game.provide_question method to return a test question
        mock_provide_question.return_value = "test_question"

        game_id = "test_game_id"
        response = self.app.get(f'/next_question/{game_id}')

        # Check the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "test_question")

        # Ensure that Game.provide_question was called with the correct arguments
        mock_provide_question.assert_called_once_with(game_id)

    @patch('app.Game.provide_question')
    def test_next_question_game_over(self, mock_provide_question):
        # Mocking the Game.provide_question method to return None (game over)
        mock_provide_question.return_value = None

        game_id = "test_game_id"
        response = self.app.get(f'/next_question/{game_id}')

        # Check the response status code and content
        self.assertEqual(response.status_code, 404)
        expected_response = {"error": "End of game"}
        self.assertEqual(response.get_json(), expected_response)

        # Ensure that Game.provide_question was called with the correct arguments
        mock_provide_question.assert_called_once_with(game_id)

    @patch('app.Game.provide_question', side_effect=Exception("Test exception"))
    def test_next_question_internal_server_error(self, mock_provide_question):
        game_id = "test_game_id"
        response = self.app.get(f'/next_question/{game_id}')

        # Check the response status code and content
        self.assertEqual(response.status_code, 500)
        expected_response = {"message": "Internal server error"}
        self.assertEqual(response.get_json(), expected_response)

        # Ensure that Game.provide_question was called with the correct arguments
        mock_provide_question.assert_called_once_with(game_id)


class TestUpdatedQuestionRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.FiftyFifty.provide_lifeline')
    def test_updated_question_success(self, mock_provide_lifeline):
        # Mocking the successful behavior of FiftyFifty.provide_lifeline
        mock_provide_lifeline.return_value = "test_updated_question"

        question_id = "test_question_id"
        response = self.app.get(f'/fifty_fifty/{question_id}')

        # Check the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "test_updated_question")

        # Ensure that FiftyFifty.provide_lifeline was called with the correct arguments
        mock_provide_lifeline.assert_called_once_with(question_id)

    @patch('app.FiftyFifty.provide_lifeline', side_effect=Exception("Test exception"))
    def test_updated_question_internal_server_error(self, mock_provide_lifeline):
        question_id = "test_question_id"
        response = self.app.get(f'/fifty_fifty/{question_id}')

        # Check the response status code and content
        self.assertEqual(response.status_code, 500)
        expected_response = {"message": "Internal server error"}
        self.assertEqual(response.get_json(), expected_response)

        # Ensure that FiftyFifty.provide_lifeline was called with the correct arguments
        mock_provide_lifeline.assert_called_once_with(question_id)


class TestGetAudienceChoiceRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.AskAudience.provide_lifeline')
    def test_get_audience_choice_success(self, mock_provide_lifeline):
        # Mocking the successful behavior of AskAudience.provide_lifeline
        mock_provide_lifeline.return_value = "test_audience_choice"

        question_id = "test_question_id"
        response = self.app.get(f'/ask_audience/{question_id}')

        # Check the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "test_audience_choice")

        # Ensure that AskAudience.provide_lifeline was called with the correct arguments
        mock_provide_lifeline.assert_called_once_with(question_id)

    @patch('app.AskAudience.provide_lifeline', side_effect=Exception("Test exception"))
    def test_get_audience_choice_internal_server_error(self, mock_provide_lifeline):
        question_id = "test_question_id"
        response = self.app.get(f'/ask_audience/{question_id}')

        # Check the response status code and content
        self.assertEqual(response.status_code, 500)
        expected_response = {"message": "Internal server error"}
        self.assertEqual(response.get_json(), expected_response)

        # Ensure that AskAudience.provide_lifeline was called with the correct arguments
        mock_provide_lifeline.assert_called_once_with(question_id)


class TestShowLeaderboardRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.Game.show_leaderboard')
    def test_show_leaderboard_success(self, mock_show_leaderboard):
        # Mocking the successful behavior of Game.show_leaderboard
        mock_show_leaderboard.return_value = {"user1": 100, "user2": 90, "user3": 80}

        response = self.app.get('/leaderboard/')

        # Check the response status code and content
        self.assertEqual(response.status_code, 200)
        expected_response = {"user1": 100, "user2": 90, "user3": 80}
        self.assertEqual(response.get_json(), expected_response)

        # Ensure that Game.show_leaderboard was called with the correct arguments
        mock_show_leaderboard.assert_called_once()

    @patch('app.Game.show_leaderboard', side_effect=Exception("Test exception"))
    def test_show_leaderboard_internal_server_error(self, mock_show_leaderboard):
        response = self.app.get('/leaderboard/')

        # Check the response status code and content
        self.assertEqual(response.status_code, 500)
        expected_response = {"message": "Internal server error"}
        self.assertEqual(response.get_json(), expected_response)

        # Ensure that Game.show_leaderboard was called with the correct arguments
        mock_show_leaderboard.assert_called_once()


if __name__ == '__main__':
    unittest.main()
