from django.contrib import admin

# Register your models here.
from .models import Question
from .models import Airbnb_listing
from .models import attribute
from .models import business
from .models import category
from .models import checkin
from .models import elite_years
from .models import friend
from .models import hours
from .models import photo
from .models import review
from .models import tip
from .models import user

admin.site.register(Question)
admin.site.register(Airbnb_listing)
admin.site.register(attribute)
admin.site.register(business)
admin.site.register(category)
admin.site.register(checkin)
admin.site.register(elite_years)
admin.site.register(friend)
admin.site.register(hours)
admin.site.register(photo)
admin.site.register(review)
admin.site.register(tip)
admin.site.register(user)
