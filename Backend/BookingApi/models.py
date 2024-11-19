from django.db import models
from Authentication.models import CustomUser


class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_participants = models.PositiveIntegerField(default=1)
    is_open = models.BooleanField(default = False)
    participants = models.ManyToManyField(CustomUser, blank = True, related_name='joined_reservations')

    def is_full(self):
        return self.participants.cout() >= self.max_participants

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=500,blank=False, null = False)
    date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=500,blank=False, null = False)
    date = models.DateTimeField(auto_now_add=True)    

class Team(models.Model):
    name = models.CharField(max_length=255)
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    participants = models.ManyToManyField(CustomUser,blank = True, related_name='teams') 


