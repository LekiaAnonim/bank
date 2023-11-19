from django.forms import ModelForm

from .models import User, Account, CreateHistory, Payment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.conf import settings

class EnrolModelForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomerPaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['account_name', 'account_number', 'bank', 'amount',
                  'receiver_email', 'routing_number', 'bank_address', 'otp']

class CreateHistoryForm(ModelForm):
    date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = CreateHistory
        fields = '__all__'
        widgets = {
            'date': DatePickerInput(format='%m/%d%Y'),
        }


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email']


class UserLoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={
        "name": "username", "class": "input100",
        "placeholder": "USER ID"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "name": "password",  "class": "input100",
        "placeholder": "Password"
    }))


class UserRegisterForm(UserCreationForm):
    """
        Creates User registration form for signing up.
    """

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)

    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={
        "name": "email", "class": "input100",
        "placeholder": "Email"
    }
    ),
        help_text='Required. Input a valid email address.'
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "name": "password1", "class": "input100",
        "placeholder": "Password"
    }
    ),
    )

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "name": "password2", "class": "input100",
        "placeholder": "Confirm Password"
    }

    ),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {

            "username": forms.TextInput(attrs={
                "name": "username", "class": "input100",
                "placeholder": "Username"
            }),


        }

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomerLoginForm(forms.Form):

    USER_ID = forms.CharField(widget=forms.TextInput(attrs={
        "name": "USER ID", "class": "input100",
        "placeholder": "USER ID"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "name": "password",  "class": "input100",
        "placeholder": "Password"
    }))
