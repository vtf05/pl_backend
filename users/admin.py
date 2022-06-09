from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

#  for login in admin pannel one need to enter mobile number starting with their country code 

from .models import User
    
class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('mobile' , 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
          (_('user_info'), {'fields': ('profile_photo','username','email')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2'),
        }),
    )
    list_display = ['username', 'first_name', 'last_name', 'is_staff']
    search_fields = ('username','mobile', 'first_name', 'last_name')
    ordering = ('mobile',)
    
    
admin.site.register(User, UserAdmin)    
    