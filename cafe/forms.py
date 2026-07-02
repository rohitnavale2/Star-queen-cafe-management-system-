from django import forms
from datetime import date
from .models import Reservation, DeliveryOrder


class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': str(date.today())})
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )

    class Meta:
        model = Reservation
        fields = ['name', 'phone', 'date', 'time', 'guests', 'special_request']
        widgets = {
            'name':           forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'phone':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXX XXXXX'}),
            'guests':         forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_guests(self):
        g = self.cleaned_data.get('guests')
        if g and (g < 1 or g > 20):
            raise forms.ValidationError("Guests must be 1-20.")
        return g

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(''.join(filter(str.isdigit, phone))) < 10:
            raise forms.ValidationError("Enter a valid phone number.")
        return phone


class DeliveryOrderForm(forms.ModelForm):
    class Meta:
        model = DeliveryOrder
        fields = ['name', 'phone', 'email', 'address', 'landmark', 'pincode', 'payment_method', 'special_note']
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control dform-input', 'placeholder': 'Your full name'}),
            'phone':   forms.TextInput(attrs={'class': 'form-control dform-input', 'placeholder': '+91 XXXXX XXXXX'}),
            'email':   forms.EmailInput(attrs={'class': 'form-control dform-input', 'placeholder': 'email@example.com (optional)'}),
            'address': forms.Textarea(attrs={'class': 'form-control dform-input', 'rows': 3, 'placeholder': 'House No., Street, Area...'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control dform-input', 'placeholder': 'Near landmark (optional)'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control dform-input', 'placeholder': '431122', 'maxlength': '10'}),
            'payment_method': forms.Select(attrs={'class': 'form-select dform-input'}),
            'special_note': forms.Textarea(attrs={'class': 'form-control dform-input', 'rows': 2, 'placeholder': 'Any special instructions...'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(''.join(filter(str.isdigit, phone))) < 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if len(''.join(filter(str.isdigit, pincode))) < 6:
            raise forms.ValidationError("Enter a valid 6-digit pincode.")
        return pincode
