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


class business(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=255, null=True, default=None)
    neighborhood = models.CharField(max_length=255, null=True, default=None)
    address = models.CharField(max_length=255, null=True, default=None)
    city = models.CharField(max_length=255, null=True, default=None)
    state = models.CharField(max_length=255, null=True, default=None)
    postal_code = models.CharField(max_length=255, null=True, default=None)
    latitude = models.FloatField(null=True, default=None)
    longitude = models.FloatField(null=True, default=None)
    stars = models.FloatField(null=True, default=None)
    review_count = models.IntegerField(null=True, default=None)
    is_open = models.IntegerField(null=True, default=None)
    def __str__(self):
        return self.name

class user(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=255, null=True, default=None)
    review_count = models.IntegerField(null=True, default=None)
    yelping_since = models.DateTimeField('date joined', null=True, default=None)
    useful = models.IntegerField(null=True, default=None)
    funny = models.IntegerField(null=True, default=None)
    cool = models.IntegerField(null=True, default=None)
    fans = models.IntegerField(null=True, default=None)
    average_stars = models.FloatField(null=True, default=None)
    compliment_hot = models.IntegerField(null=True, default=None)
    compliment_more = models.IntegerField(null=True, default=None)
    compliment_profile = models.IntegerField(null=True, default=None)
    compliment_cute = models.IntegerField(null=True, default=None)
    compliment_list = models.IntegerField(null=True, default=None)
    compliment_note = models.IntegerField(null=True, default=None)
    compliment_plain = models.IntegerField(null=True, default=None)
    compliment_cool = models.IntegerField(null=True, default=None)
    compliment_funny = models.IntegerField(null=True, default=None)
    compliment_writer = models.IntegerField(null=True, default=None)
    compliment_photos = models.IntegerField(null=True, default=None)
    def __str__(self):
        return self.name

class attribute(models.Model):
    business_id = models.ForeignKey(business, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, null=True, default=None)
    value = models.TextField()

class category(models.Model):
    business_id = models.ForeignKey(business, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=255, null=True, default=None)

class checkin(models.Model):
    business_id = models.ForeignKey(business, on_delete=models.DO_NOTHING)
    date = models.CharField(max_length=255, null=True, default=None)
    count = models.IntegerField(null=True, default=None)

class elite_years(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    year = models.IntegerField(null=True, default=None)

class friend(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    friend_id = models.CharField(max_length=22, null=True, default=None)

class hours(models.Model):
    hours = models.CharField(max_length=255, null=True, default=None)
    business_id = models.ForeignKey(business, on_delete=models.DO_NOTHING)

class photo(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    business_id = models.ForeignKey(business, on_delete=models.DO_NOTHING)
    caption = models.CharField(max_length=255, null=True, default=None)
    label = models.CharField(max_length=255, null=True, default=None)
    
class review(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    stars = models.IntegerField(null=True, default=None)
    date = models.DateTimeField('date published', null=True, default=None)
    text = models.TextField()
    useful = models.IntegerField(null=True, default=None)
    funny = models.IntegerField(null=True, default=None)
    cool = models.IntegerField(null=True, default=None)
    business_id = models.ForeignKey(business, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(user, on_delete=models.DO_NOTHING)

class tip(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    business_id = models.ForeignKey(business, on_delete=models.DO_NOTHING)
    text = models.TextField()
    date = models.DateTimeField('date published', null=True, default=None)
    likes = models.IntegerField(null=True, default=None)
