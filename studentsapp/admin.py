from django.contrib import admin
from studentsapp import models as s_model

# Register your models here.
admin.site.register(s_model.User)
admin.site.register(s_model.Events)
admin.site.register(s_model.EventsRegistered)
admin.site.register(s_model.Sports)
admin.site.register(s_model.SportsRegistered)
admin.site.register(s_model.Accommodation)
