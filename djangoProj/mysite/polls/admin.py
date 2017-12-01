from django.contrib import admin

# Register your models here.
from .models import Question
from .models import Airbnb_listing

admin.site.register(Question)
admin.site.register(Airbnb_listing)
