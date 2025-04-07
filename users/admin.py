from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_doctor')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Doctor Status'), {'fields': ('is_doctor',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Only superusers can edit the Permissions section
        if not request.user.is_superuser and obj is not None:
            return [fs for fs in fieldsets if fs[0] != _('Permissions')]
        return fieldsets
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Non-superusers should not see other staff/superusers
        if not request.user.is_superuser:
            return qs.filter(is_staff=False, is_superuser=False)
        return qs
    
    def has_change_permission(self, request, obj=None):
        # Prevent non-superusers from editing superusers
        if obj and not request.user.is_superuser and obj.is_superuser:
            return False
        return super().has_change_permission(request, obj)
