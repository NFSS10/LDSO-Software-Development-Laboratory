from django.contrib import admin
from .models import Event, EventType, EventParticipation, EventImages

admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(EventParticipation)
admin.site.register(EventImages)
