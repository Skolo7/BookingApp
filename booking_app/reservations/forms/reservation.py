from django import forms
from django.core.exceptions import ValidationError

from ..models import Reservation


class DateInput(forms.DateInput):
    input_type = 'date'


class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Select start date'}
            ),
            'end_date': DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'placeholder': 'Select end date',
                }
            ),
        }

    def clean(self):
        cleaned_date = super().clean()
        start_date = cleaned_date.get('start_date')
        end_date = cleaned_date.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise ValidationError('Start date cannot be after end date.')
        return cleaned_date


# class ReserveParkingForm(forms.ModelForm):
#     class Meta:
#         model = Reservation
#         fields = ['start_date', 'end_date']
#         widgets


class FilterAvailabilityForm(forms.Form):  # FilterDesksForm
    start_date = forms.DateField(
        widget=DateInput(
            attrs={'class': 'form-control', 'placeholder': 'Select start date'}
        )
    )
    end_date = forms.DateField(
        widget=DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select end date',
            }
        )
    )

    def clean(self):
        cleaned_date = super().clean()
        start_date = cleaned_date.get('start_date')
        end_date = cleaned_date.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise ValidationError('Start date cannot be after end date.')
        return cleaned_date


class SingleReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date']
        widgets = {
            'start_date': DateInput,
        }
