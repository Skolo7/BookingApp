from datetime import date

from django import forms
from django.forms.widgets import DateInput


class DateForm(forms.Form):
    my_date = forms.DateField(
        widget=DateInput(
            attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}
        )
    )
