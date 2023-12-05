"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, EventGamer
from rest_framework.decorators import action
from django.db.models import Q

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
        events = Event.objects.all()
        # events = Event.objects.annotate(attendees_count=Count('joined'))
        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)

        
        for event in events:
            # Check to see if there is a row in the Event Games table that has the passed in gamer and event
            event.joined = len(EventGamer.objects.filter(
            gamer=gamer, event=event)) > 0
            event.attendees_count = len(EventGamer.objects.filter(
            gamer=gamer, event=event))
        serializer = EventSerializer(events, many=True)
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
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
        
        uid = request.META['HTTP_AUTHORIZATION']

        gamer = Gamer.objects.get(uid=uid)
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.create(
            gamer=gamer,
            event=event
        )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""
        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)
        event = Event.objects.get(pk=pk)
        eventgamer = EventGamer.objects.filter(gamer_id=gamer, event_id=event)
        eventgamer.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
class EventSerializer(serializers.ModelSerializer):
  attendees_count = serializers.IntegerField(default=None)
  
  class Meta:
    model = Event
    fields = ('id', 'description', 'date', 'time', 'game_id', 'organizer_id', 'joined', 'attendees_count' )
