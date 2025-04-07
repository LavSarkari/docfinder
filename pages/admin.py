from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import TeamMember, AdminStaff

User = get_user_model()

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'position')
    list_filter = ('position',)
    ordering = ('order',)

@admin.register(AdminStaff)
class AdminStaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'permissions', 'is_active', 'added_by', 'created_at')
    list_filter = ('permissions', 'is_active')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'role')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only superusers can see all admin staff
        if not request.user.is_superuser:
            return qs.filter(added_by=request.user)
        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
        
        # Update user permissions based on AdminStaff permissions
        user = obj.user
        user.is_staff = True
        
        if obj.permissions == 'full':
            user.is_superuser = True
        else:
            user.is_superuser = False
            
        user.save()
