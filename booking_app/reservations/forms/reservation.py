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
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_date = cleaned_data.get('start_date')
    #     end_date = cleaned_data.get('end_date')
    #     if start_date and end_date and start_date > end_date:
    #         raise ValidationError('Start date cannot be after end date.')
    #     return cleaned_data



class FilterAvailabilityForm(forms.Form):
    # start_date = forms.DateField(
    #     widget=DateInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Select start date'}
    #     )
    # )
    # end_date = forms.DateField(
    #     widget=DateInput(
    #         attrs={
    #             'class': 'form-control',
    #             'type': 'date',
    #             'placeholder': 'Select end date',
    #         }
    #     )
    # )

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

    # def clean(self):
    #     cleaned_date = super().clean()
    #     start_date = cleaned_date.get('start_date')
    #     end_date = cleaned_date.get('end_date')
    #     if start_date and end_date and start_date > end_date:
    #         raise ValidationError('Start date cannot be after end date.')
    #     return cleaned_date


class SingleReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date']
        widgets = {
            'start_date': DateInput,
        }
