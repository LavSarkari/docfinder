from django.contrib import admin
from .models import Doctor, Specialization, DoctorDocument

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'doctor_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_specializations', 'registration_number', 'experience', 'clinic_city', 'verified']
    list_filter = ['verified', 'clinic_city', 'clinic_state', 'experience']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'registration_number']
    list_editable = ['verified']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_specializations(self, obj):
        return ", ".join([s.name for s in obj.specializations.all()])
    get_specializations.short_description = 'Specializations'

@admin.register(DoctorDocument)
class DoctorDocumentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'title', 'uploaded_at', 'verified']
    list_filter = ['verified', 'uploaded_at']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name', 'title']
    list_editable = ['verified']
    readonly_fields = ['uploaded_at']
