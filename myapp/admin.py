from django.contrib import admin
from .models import Resource, Announcement, Mark, Query

admin.site.register(Resource)
admin.site.register(Announcement)
admin.site.register(Mark)



class QueryAdmin(admin.ModelAdmin):
    list_display = ('student', 'message', 'timestamp')
