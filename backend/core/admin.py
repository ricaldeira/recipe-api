from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models
from address import models as address_models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    ]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
admin.site.register(models.BusinessUser)

admin.site.register(address_models.Address)
admin.site.register(address_models.City)
admin.site.register(address_models.State)
