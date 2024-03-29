"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        games = Game.objects.annotate(event_count=Count('events'))
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(uid=request.data["userId"])
        game_type = GameType.objects.get(pk=request.data["gameType"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["numberOfPlayers"],
            skill_level=request.data["skillLevel"],
            game_type=game_type,
            gamer=gamer,
        )
        serializer = GameSerializer(game, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]
        
        game_type = GameType.objects.get(pk=request.data["gameType"])
        game.game_type = game_type
        game.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
class GameSerializer(serializers.ModelSerializer):
    event_count = serializers.IntegerField(default=None)
  
    class Meta:
      model = Game
      fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type_id', 'gamer_id', 'event_count' )
