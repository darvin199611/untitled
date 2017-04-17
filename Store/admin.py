from django.contrib import admin
from .models import Market, Stuff, Sale
from .models import UserProfile


class MarketStuffInline (admin.TabularInline):
    model = Stuff
    extra = 0


class MarketAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Market._meta.fields]
#    inlines = [MarketStuffInline]

    class Meta:
        model = Market

admin.site.register(Market, MarketAdmin)


class UserProfileAdmin (admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields]

    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)


class StuffAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Stuff._meta.fields]

    class Meta:
        model = Stuff

admin.site.register(Stuff, StuffAdmin)


class SaleAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Sale._meta.fields]

    class Meta:
        model = Sale

admin.site.register(Sale, SaleAdmin)
