from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from ..models import Reservation


class DateInput(forms.DateInput):
    input_type = 'date'


class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today().strftime('%Y-%m-%d')
        default_attrs = {
            'class': 'form-control',
            'min': today,
            'value': today
        }

        self.fields['start_date'].widget = DateInput(
            attrs={**default_attrs, 'placeholder': 'Select start date'}
        )
        self.fields['end_date'].widget = DateInput(
            attrs={**default_attrs, 'placeholder': 'Select end date'}
        )


    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if all([start_date, end_date]) and start_date > end_date:
            raise ValidationError('Start date cannot be after end date.')
        
        return cleaned_data


class FilterAvailabilityForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_attrs = {
            'class': 'form-control',
        }

        self.fields['start_date'] = forms.DateField(
            widget=DateInput(
                attrs={**default_attrs, 'placeholder': 'Select start date'}
            )
        )
        self.fields['end_date'] = forms.DateField(
            widget=DateInput(
                attrs={**default_attrs, 'placeholder': 'Select end date'}
            )
        )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if all([start_date, end_date]) and start_date > end_date:
            raise ValidationError('Start date cannot be after end date.')
        
        return cleaned_data

class SingleReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date']
        widgets = {
            'start_date': DateInput,
        }
