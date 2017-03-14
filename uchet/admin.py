from django.contrib import admin
from .models import Market,Stuff
from .models import UserProfile


admin.site.register(Market)
admin.site.register(UserProfile)
admin.site.register(Stuff)
