from django import forms
from .models import Doctor, Specialization, DoctorDocument
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, ButtonHolder
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget

class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user', 'verified', 'created_at', 'updated_at']
        widgets = {
            'specializations': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'bio': CKEditorWidget(),
            'experience': forms.Select(attrs={'class': 'form-select'}),
            'clinic_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'clinic_city': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic_state': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic_pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'available_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Monday, Tuesday, Wednesday...'}),
            'available_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '9:00 AM - 1:00 PM, 5:00 PM - 8:00 PM...'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'registration_number': _('Medical Registration Number'),
            'bio': _('Professional Bio'),
            'available_days': _('Available Days (Comma separated)'),
            'available_hours': _('Available Hours (Comma separated)'),
        }
        help_texts = {
            'specializations': _('Hold Ctrl/Cmd to select multiple specializations'),
            'registration_number': _('Your medical council registration number'),
            'available_days': _('Enter days of the week you are available, separated by commas'),
            'available_hours': _('Enter time slots when you are available, separated by commas'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('specializations', css_class='col-md-6'),
                Column('registration_number', css_class='col-md-6'),
            ),
            Row(
                Column('qualification', css_class='col-md-6'),
                Column('experience', css_class='col-md-6'),
            ),
            'bio',
            Row(
                Column('clinic_address', css_class='col-md-12'),
            ),
            Row(
                Column('clinic_city', css_class='col-md-4'),
                Column('clinic_state', css_class='col-md-4'),
                Column('clinic_pincode', css_class='col-md-4'),
            ),
            Row(
                Column('consultation_fee', css_class='col-md-6'),
                Column('profile_picture', css_class='col-md-6'),
            ),
            Row(
                Column('available_days', css_class='col-md-6'),
                Column('available_hours', css_class='col-md-6'),
            ),
            ButtonHolder(
                Submit('submit', 'Register', css_class='btn-primary')
            )
        )

class DoctorDocumentForm(forms.ModelForm):
    class Meta:
        model = DoctorDocument
        fields = ['title', 'document']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'document',
            ButtonHolder(
                Submit('submit', 'Upload Document', css_class='btn-primary')
            )
        )

class DoctorProfileEditForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'specializations', 'qualification', 'experience', 'bio',
            'clinic_address', 'clinic_city', 'clinic_state', 'clinic_pincode',
            'consultation_fee', 'available_days', 'available_hours', 'profile_picture'
        ]
        widgets = {
            'specializations': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'bio': CKEditorWidget(),
            'experience': forms.Select(attrs={'class': 'form-select'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'clinic_city': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic_state': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic_pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Monday, Tuesday, Wednesday...'}),
            'available_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '9:00 AM - 1:00 PM, 5:00 PM - 8:00 PM...'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'bio': _('Professional Bio'),
            'available_days': _('Available Days (Comma separated)'),
            'available_hours': _('Available Hours (Comma separated)'),
        }
        help_texts = {
            'specializations': _('Hold Ctrl/Cmd to select multiple specializations'),
            'available_days': _('Enter days of the week you are available, separated by commas'),
            'available_hours': _('Enter time slots when you are available, separated by commas'),
        } 