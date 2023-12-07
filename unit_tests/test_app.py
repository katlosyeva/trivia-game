import unittest
import json
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify
from werkzeug.test import Client
from app import app, User, Game


class TestAddGameRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_successful_game_creation(self):
        user_name = "helen"
        user_data = {"user_name": user_name}
        response = self.app.post('/add_new_game', json=user_data)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn('player_id', data)
        self.assertIn('game_id', data)
        self.assertIn('question', data)

    def test_failure_missing_user_name(self):
        response = self.app.post('/add_new_game', json={})
        self.assertEqual(response.status_code, 400)  # Assuming a 400 Bad Request status code

    def test_failure_exceeding_maximum_username_length(self):
        long_user_name = "b" * 41  # Assuming a username longer than 40 characters
        user_data_long = {"user_name": long_user_name}
        response_long = self.app.post('/add_new_game', json=user_data_long)
        self.assertEqual(response_long.status_code, 400)  # Assuming a 400 Bad Request status code
        data_long = json.loads(response_long.get_data(as_text=True))
        self.assertIn('message', data_long)
        self.assertEqual(data_long['message'], 'User name must be between 1 and 40 characters')


class TestCheckAnswerRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_check_answer_route(self):
        answer_data = {
            "game_id": 1,
            "answer": "The Bahamas Archipelago",
            "question_id": 46
        }
        response = self.app.put('/check_answer', json=answer_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('score', response.get_data(as_text=True))
        self.assertIn('correct_answer', response.get_data(as_text=True))
        self.assertIn('result', response.get_data(as_text=True))


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
