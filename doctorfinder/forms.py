from django import forms
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, ButtonHolder, Field

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("First Name"),
                "autocomplete": "given-name",
            }
        )
    )
    
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Last Name"),
                "autocomplete": "family-name",
            }
        )
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='col-md-12'),
            ),
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('username', css_class='col-md-12'),
            ),
            Row(
                Column('password1', css_class='col-md-12'),
            ),
            Row(
                Column('password2', css_class='col-md-12'),
            ),
        )
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        return user 