from django.contrib import admin

from api.models import User, Environment, Agent, Level, Event

admin.site.register(User)
admin.site.register(Environment)
admin.site.register(Agent)
admin.site.register(Level)
admin.site.register(Event)
