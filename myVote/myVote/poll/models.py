from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
    subject = models.CharField(max_length=80)
    detail = models.TextField(max_length=200)
    picture = models.ImageField(upload_to='gallery', null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    password = models.CharField(max_length=30,blank=True, null=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=True)

class Poll_Choice(models.Model):
    subject = models.CharField(max_length=80)
    image = models.ImageField(upload_to='gallery', null=True)
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)

class Poll_Vote(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Poll_Choice, on_delete=models.CASCADE)
    vote_by = models.ForeignKey(User, on_delete=models.CASCADE)

