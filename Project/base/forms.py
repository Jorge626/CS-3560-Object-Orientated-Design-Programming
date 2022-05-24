from django import forms
from django.forms import ModelForm
from .models import Account, Bill, Rate


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ('customerID', 'serviceAddress',
                  'serviceAddress2', 'city', 'state', 'zipcode')
        labels = {
            'customerID': 'Customer ID',
            'serviceAddress': 'Service Address',
            'serviceAddress2': 'Service Address 2',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zip Code',
        }

        widgets = {
            'customerID': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer ID #'}),
            'serviceAddress': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address of Account'}),
            'serviceAddress2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment, studio, or floor'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City of Account'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '5-digit zip'})
        }


class UsageForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('accountID', 'readingDate',
                  'currentReading')
        labels = {
            'accountID': 'Account ID',
            'readingDate': 'Reading Date',
            'currentReading': 'Current Meter Reading',
        }

        widgets = {
            'accountID': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account ID #'}),
            'readingDate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date the meter reading was recorded'}),
            'currentReading': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current reading'})
        }


class SuspensionForm(ModelForm):
    class Meta:
        model = Account
        fields = ('serviceAddress', 'suspendDate', 'suspend')
        labels = {
            'serviceAddress': 'Service address',
            'suspendDate': 'Suspension Date',
            'suspend': 'Suspension',
        }

        widgets = {
            'serviceAddress': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer ID #'}),
            'suspendDate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date of suspension'}),
            'suspend': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type True or False'})
        }


class RateForm(ModelForm):
    class Meta:
        model = Rate
        fields = ('tierID', 'price')  # , 'theRange')
        labels = {
            'tierID': 'Tier ID',
            'price': 'Price',
            # 'theRange': 'Range',
        }

        widgets = {
            'tierID': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tier ID #'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price of the Rate'}),
            # 'theRange': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'The Range'})
        }
