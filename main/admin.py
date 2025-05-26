from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Construction, Model3D

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_verified', 'is_staff')    
    list_filter = ('is_active', 'is_verified', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_verified', 'is_staff', 'is_superuser')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Construction)
class ConstructionAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'type', 'demolished')


@admin.register(Model3D)
class Model3DAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'construction', 'latitude', 'longitude', 'altitude', 'uploaded')
    list_filter  = ('construction',)