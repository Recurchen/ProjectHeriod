from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class NewRecordForm(forms.Form):

    date = forms.DateField()
    period = forms.IntegerField()

    def clean(self):
        data = super().clean()

        # if len(data.get('name')) == 0:
        #     self.add_error('name', 'This field is required')
        # if len(data.get('transit_num')) == 0:
        #     self.add_error('transit_num', 'This field is required')
        # if len(data.get('address')) == 0:
        #     self.add_error('address', 'This field is required')
        # if len(data.get('email')) == 0:
        #     self.add_error('email', 'This field is required')

        # try:
        #     validate_email(data.get('email'))
        # except ValidationError:
        #     self.add_error('email', 'Enter a valid email address')

        return data
