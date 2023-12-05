from django.db import models

class Event(models.Model):
  
  game = models.ForeignKey('game', on_delete=models.CASCADE, related_name='events')
  description = models.CharField(max_length=50)
  date = models.DateField(auto_now=False, auto_now_add=False)
  time = models.TimeField()
  organizer = models.ForeignKey('gamer', on_delete=models.CASCADE, related_name='events')
  
  @property
  def joined(self):
    return self.__joined

  @joined.setter
  def joined(self, value):
    self.__joined = value