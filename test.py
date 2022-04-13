from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_word_present(self):

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['C', 'A', 'T', 'O', 'P'], ['C', 'A', 'T', 'O', 'P'], [
                    'C', 'A', 'T', 'O', 'P'], ['C', 'A', 'T', 'O', 'P'], ['C', 'A', 'T', 'O', 'P']]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_word_absent(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=elephant')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_english_word(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=asdfasd')
        self.assertEqual(response.json['result'], 'not-word')
