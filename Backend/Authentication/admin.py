from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm 
    form = CustomUserChangeForm 
    
    model = CustomUser
    
    list_display = ['email','firstname','lastname','is_staff','is_active']
    list_filter = ['email','is_staff','is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('firstname','lastname')}),
        ('Permissions', {'fields': ('is_active','is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','firstname','lastname', 'password1', 'password2','is_staff','is_active','groups','user_permissions')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    
    
admin.site.register(CustomUser, CustomUserAdmin)