import unittest
import json
from app import app


class TestAddGameRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_add_game_route(self):
        user_name = "helen"
        user_data = {"user_name": user_name}
        response = self.app.post('/add_new_game', json=user_data)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn('player_id', data)
        self.assertIn('game_id', data)
        self.assertIn('question', data)


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