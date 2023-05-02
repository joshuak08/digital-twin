from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ModelForm, forms
from django import forms


# from .models import SimInput


# Create Sim Input form
class SimInputForm(forms.Form):
    # Want to try to create 4 different fields and merge them all into 1 list for particulates in each tank
    tank0 = forms.FloatField(label='Amount of pre-existing particulate in tank 1 [Max value: 11000000] (mg)',
                             validators=[MinValueValidator(0, message="Please enter a valid value larger than 0."),
                                         MaxValueValidator(1100000, message="Please enter a value smaller than 11000000.")])
    tank1 = forms.FloatField(label='Amount of pre-existing particulate in tank 2 [Max value: 11000000] (mg)',
                             validators=[MinValueValidator(0, message="Please enter a valid value larger than 0."),
                                         MaxValueValidator(1100000, message="Please enter a value smaller than 11000000.")])
    tank2 = forms.FloatField(label='Amount of pre-existing particulate in tank 3 [Max value: 11000000] (mg)',
                             validators=[MinValueValidator(0, message="Please enter a valid value larger than 0."),
                                         MaxValueValidator(1100000, message="Please enter a value smaller than 11000000.")])
    tank3 = forms.FloatField(label='Amount of pre-existing particulate in tank 4 [Max value: 11000000] (mg)',
                             validators=[MinValueValidator(0, message="Please enter a valid value larger than 0."),
                                         MaxValueValidator(1100000, message="Please enter a value smaller than 11000000.")])
    average_flow = forms.FloatField(label='Average Flow (m^3/s)',
                                    validators=[MinValueValidator(0, message="Please enter a valid value larger than 0."),
                                                MaxValueValidator(0.5, message="Please enter a value smaller than 0.5")])
    average_tss = forms.FloatField(label='Amount of particulate in waste water (mg/l), [Average is 252]')
    sim_length = forms.IntegerField(label='Length of time for simulation (s)')
    # If checked data will be displayed as 'on'/'off' instead of true or false
    # testing = forms.BooleanField(label='Is this part of testing?')
    # class Meta:
    #     model = SimInput
    #     fields = '__all__'

    # def clean_length(self):
    #     length = self.cleaned_data.get('sim_length')
    #     if length < 0:
    #         print('asdf')
    #         raise forms.ValidationError('Please enter positive asdf value.')
    #         print('asldkfj')
    #     return length
