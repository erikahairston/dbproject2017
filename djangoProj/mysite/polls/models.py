import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.

class Airbnb_listing(models.Model):
    room_id = models.IntegerField(default=0)
    survey_id = models.IntegerField(default=0)
    host_id = models.IntegerField(default=0)
    room_type = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    borough = models.CharField(max_length=500)
    neighborhood = models.CharField(max_length=500)
    reviews = models.IntegerField(default=0)
    overall_satisfaction = models.FloatField(default=0)
    accommodates = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    minstay = models.IntegerField(default=0)
    name = models.CharField(max_length=500)
    last_modified = models.CharField(max_length=500)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
