from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Game, Gamer
from levelupapi.views.game import GameSerializer

class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['gamers', 'game_types', 'games', 'events']
    
    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        # token = Token.objects.get(user=self.gamer.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    def test_get_game(self):
        # Grab a game object from the database
          game = Game.objects.first()

          url = f'/games/{game.id}'

          response = self.client.get(url)

          self.assertEqual(status.HTTP_200_OK, response.status_code)

          # Like before, run the game through the serializer that's being used in view
          expected = GameSerializer(game)

          # Assert that the response matches the expected return data
          self.assertEqual(expected.data, response.data)
          
    def test_list_games(self):
        """Test list games"""
        url = '/games'

        response = self.client.get(url)
        
        # Get all the games in the database and serialize them to get the expected output
        all_games = Game.objects.all()
        expected = GameSerializer(all_games, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)
        
    def test_delete_game(self):
        """Test delete game"""
        game = Game.objects.first()

        url = f'/games/{game.id}'
        response = self.client.delete(game.id)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

        # Test that it was deleted by trying to _get_ the game
        # The response should return a 404
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)