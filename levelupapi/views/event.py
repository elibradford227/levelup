"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
      """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
      # print(request.data)
      # organizer = Gamer.objects.get(uid=request.data["uid"])
      # game = Game.objects.get(pk=request.data["gameTypeId"])
      
      print(request.data)

      event = Event.objects.create(
          description=request.data["description"],
          date=request.data["date"],
          time=request.data["time"],
          game_id=request.data["game"],
          organizer_id=request.data["organizer"],
      )
      print(request.data)
      serializer = EventSerializer(event, many=False)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        
        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        game = Game.objects.get(pk=request.data['game'])
        event.game = game
        organizer = Gamer.objects.get(pk=request.data['organizer'])
        event.organizer = organizer

        event.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
class EventSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Event
    fields = ('id', 'description', 'date', 'time', 'game_id', 'organizer_id' )
