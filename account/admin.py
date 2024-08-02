from django.contrib import admin
from .models import User, Profile
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (str, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets = (
    #     (str, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'password1', 'password2'),
    #     }),
    # )
    list_display = ('email', 'username', 'is_active', 'is_superuser')
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')


admin.site.register(Profile)
