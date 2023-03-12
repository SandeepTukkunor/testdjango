from django.contrib import admin
from django.contrib.auth import admin as auth_admin

# Register your models here.
from test.user.forms import UserAdminCreationForm, UserAdminChangeForm
from test.user.models import User
class UserAdmin(auth_admin.UserAdmin):
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'is_verified',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_verified',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_verified',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)

