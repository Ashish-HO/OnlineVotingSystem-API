from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import timedelta

# Create your models here.


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
    imagelink = models.CharField(max_length=255)

    # many candidate are related to single post ,
    # on delete cascade means if post is deleted then candidate will also be deleted
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="candidate")

    def __str__(self):
        return self.name


class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.title


class ElectionSetting(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now().date())
    end_date = models.DateField(default=timezone.now().date() + timedelta(days=2))

    def __str__(self):
        return self.name
