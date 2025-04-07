from django import forms
from .models import Review
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, ButtonHolder

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment', 'verified_visit']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('rating', css_class='col-md-12'),
            ),
            Row(
                Column('title', css_class='col-md-12'),
            ),
            Row(
                Column('comment', css_class='col-md-12'),
            ),
            Row(
                Column('verified_visit', css_class='col-md-12'),
            ),
            ButtonHolder(
                Submit('submit', 'Submit Review', css_class='btn-primary')
            )
        ) 