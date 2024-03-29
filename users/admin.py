from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import *


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    list_display = ('phone','id', 'role')
    list_filter = ('role',)
    fieldsets = (
        (None, {"fields": ('phone', 'password'),}),
        ("Personal info", {"fields": ('company', 'role', 'name', 'email','avatar', 
                        'birth_date', 'country', 'city','location', 'created_at', 'last_online')}),
        ("tp", {"fields": ('price_type', 'type_price', 'storage', 'sector_order', 'order_sector', 'show_plan', 'show_plan_date')}),
        ("Юр info", {"fields": ('bin_iin', 'credit', 'debt', 'paymets', 'galleon', 'agent')}),
        ("Permissions", {"fields": ('is_moder', 'is_staff', 'is_active')})
    )
    readonly_fields = ('created_at', 'show_plan_date')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
            ),
    )

    search_fields = ('phone',)
    ordering = ('phone',)

admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP)
admin.site.register(Company)

