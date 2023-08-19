from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_initialize_session(self):
        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 302)  # Redirects to /game

    def test_game_route(self):
        with self.client as client:
            response = client.get('/game')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<table>', response.data)
    #so here im implementing it to check the board positions and make sure that its word validity
    #and call to the word.txt works
    #setting up a static bored so that it is a constant in the testing.
    def test_check_word_valid(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ['A', 'B', 'C', 'D', 'E'],
                    ['F', 'G', 'H', 'I', 'J'],
                    ['K', 'L', 'M', 'N', 'O'],
                    ['P', 'Q', 'R', 'S', 'T'],
                    ['U', 'V', 'W', 'X', 'Y']
                ]
            response = client.post('/check-word', json={'guess': 'DOG'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

    def test_check_word_invalid(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ['A', 'B', 'C', 'D', 'E'],
                    ['F', 'G', 'H', 'I', 'J'],
                    ['K', 'L', 'M', 'N', 'O'],
                    ['P', 'Q', 'R', 'S', 'T'],
                    ['U', 'V', 'W', 'X', 'Y']
                ]
            response = client.post('/check-word', json={'guess': 'XYZ'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-on-board')

if __name__ == '__main__':
    unittest.main()
