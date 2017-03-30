from django.contrib import admin
from .models import Market,Stuff, Sale
from .models import UserProfile


admin.site.register(Market)
admin.site.register(UserProfile)
admin.site.register(Stuff)
admin.site.register(Sale)
