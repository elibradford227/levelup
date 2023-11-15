from django.db import models

class Game(models.Model):
  
  game_type = models.ForeignKey('gametype', on_delete=models.CASCADE, related_name='games')
  title = models.CharField(max_length=50)
  maker = models.CharField(max_length=50)
  gamer = models.ForeignKey('gamer', on_delete=models.CASCADE, related_name='gamers')
  number_of_players = models.IntegerField() 
  skill_level = models.IntegerField() 