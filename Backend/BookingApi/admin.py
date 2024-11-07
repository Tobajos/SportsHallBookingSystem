from django.contrib import admin
from .models import Reservation, Post, Comment

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date', 'start_time', 'end_time', 'max_participants', 'is_open']
    list_filter = ['is_open', 'date', 'user']
    fields = ['user', 'date', 'start_time', 'end_time', 'max_participants', 'is_open', 'participants']
    filter_horizontal = ['participants']

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'date']
    list_filter = ['date', 'user']
    



admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
