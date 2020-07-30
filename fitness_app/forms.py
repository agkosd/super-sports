from .models import *
from django import forms
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


# LoginForm is a template for user login.
# It has required fields: username, and password
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


# ProfileForm is a template for user profile
# It requires users to input their height and DOB
class ProfileForm(forms.ModelForm):
    height = forms.DecimalField(label='Height (cm)')
    DOB = forms.DateField(label='DOB:', widget=forms.SelectDateWidget(years=range(1960, datetime.date.today().year)))

    class Meta:
        model = UserStats
        fields = [
            'height',
            'DOB'
        ]

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


# SignUpForm is a template for user sign up
# It requires users to input their username, first_name, last_name, email, height, DOB
# , and password two times for confirmation.
class SignUpForm(UserCreationForm):
    height = forms.DecimalField(label='Height (cm)')
    DOB = forms.DateField(label='Date of birth:', widget=forms.SelectDateWidget(years=range(1960, datetime.date.today().year)))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'height', 'DOB', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
        }

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


# UserEditForm is a template for user editing
# User has to type in the correct password to edit their information
class UserEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        passw = self.cleaned_data['password']
        if not authenticate(username=self.user.username, password=passw):
            raise forms.ValidationError("Incorrect password!")
        return passw

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


# LoggerForm is a template for editing Users' strengthWorkout stats.
# It uses current date as the workout_date
class LoggerForm(forms.ModelForm):
    workout_date = forms.DateField(label='Workout date:',
                                   widget=forms.SelectDateWidget(years=range(1960, datetime.date.today().year + 1)),
                                   initial=timezone.now())
    workout_weight = forms.DecimalField(label='Workout weight (kg)')

    class Meta:
        model = StrengthWorkout
        fields = [
            'workout_name',
            'workout_date',
            'sets',
            'reps',
            'workout_weight',
        ]

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'



# This class generates a form for calcukating the user's Ideal Caloric Intake measured in kCal.
# This value is generated according to the user's height, weight, age and activity level
class CalculatorForm(forms.Form):
    ACTIVITY_CHOICES = [
        ('0', '0 times/week'),
        ('1', '1-2 times/week'),
        ('2', '6-7 times/week'),
        ('3', '2 times/day')
    ]
    age = forms.IntegerField(label='Age', max_value=100, min_value=10)
    height = forms.IntegerField(label='Height (cm)', max_value=250, min_value=10)
    weight = forms.IntegerField(label='Weight (kg)', max_value=350, min_value=0)
    activity = forms.CharField(label='Activity Level (How often do you work out?)',
                               widget=forms.Select(choices=ACTIVITY_CHOICES))


# SelectExe is a template for user to select workouts from the available ones in the fitness_app
class SelectExe(forms.Form):
    workout_name = forms.ModelChoiceField(queryset=WorkoutType.objects.all())
    workout_name = forms.ModelChoiceField(queryset=WorkoutType.objects.all())

    class Meta:
        fields = ['workout_name']


# StatsForm is a template for using users' stats
# to show the graphs. It records users' bodyweight, fat, and calorie_intake.
class StatsForm(forms.ModelForm):
    date = forms.DateField(label='Date',
                           widget=forms.SelectDateWidget(years=range(1960, datetime.date.today().year + 1)),
                           initial=timezone.now())
    bodyweight = forms.DecimalField(label='Weight (kg)')
    fat = forms.DecimalField(label='Body fat %')
    calorie_intake = forms.DecimalField(label='Average daily calorie intake')
    class Meta:
        model = StatsOverTime
        fields = [
            'date',
            'bodyweight',
            'fat',
            'calorie_intake'
        ]

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


# WeightForm is a template for recording users' target weight
class WeightForm(forms.ModelForm):

    weight_target = forms.DecimalField(label='Weight target (kg)')
    class Meta:
        model = WeightGoals
        fields = [
            'weight_target',
        ]

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


# StrengthForm is a template for recording users' target weight for each workout
class StrengthForm(forms.ModelForm):

    strength_target = forms.DecimalField(label='Strength target (kg)')
    class Meta:
        model = StrengthGoals
        fields = [
            'workout_name',
            'strength_target',
        ]

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


# FatForm is a template for users to set their target fat goal
class FatForm(forms.ModelForm):
    class Meta:
        model = FatGoals
        fields = [
            'fat_target',
        ]

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'

# TDEE form is for editing the users TDEE and adding their growth goal
class TDEEForm(forms.ModelForm):
    ACTIVITY_CHOICES = [
        ('Maintain', 'Keep weight stable.'),
        ('Bulk', 'Incresae weight'),
        ('Cut', 'Decrease weight')
    ]
    goal = forms.ChoiceField(choices=ACTIVITY_CHOICES)
    class Meta:
        model = TDEE
        fields = [
            'tdee',
            'goal',
        ]

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'
### End forms for goals page
