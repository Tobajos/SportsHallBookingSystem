from django.contrib import admin
from .models import Reservation, Post


class ReservationAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'user', 'date', 'start_time', 'end_time', 'max_participants', 'is_open']
    
    
    filter_horizontal = ['participants']

    
    fields = ['user', 'date', 'start_time', 'end_time', 'max_participants', 'is_open', 'participants']

    
    list_filter = ['is_open', 'date', 'user']

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Post)