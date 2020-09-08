from django.contrib import admin
from .models import Event, Preferences, Interested
# Register your models here.
admin.site.register(Event)
admin.site.register(Preferences)
admin.site.register(Interested)
