from django import forms
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import AuthenticationForm

class UserRegisterForm(forms.ModelForm):
    zip_code = forms.CharField(max_length=50)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'zip_code']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'email',
            'zip_code',
            Submit('submit', 'Register', css_class='btn btn-outline-info')
        )

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['zip_code'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email')
    zip_code = forms.CharField(label='Zip Code', widget=forms.PasswordInput)
    authenticated_user = None

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()  
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username_or_email',
            'zip_code',
            Submit('submit', 'Login', css_class='btn btn-outline-info')
        )   

        super(UserLoginForm, self).__init__(*args, **kwargs)
         
    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        zip_code = self.cleaned_data.get('zip_code')

        user = authenticate(username=username_or_email, password=zip_code)
        if user is None:
            user = authenticate(username=CustomUser.objects.get(username=username_or_email), password=zip_code)
        if user is None:
            raise forms.ValidationError('Invalid username/email or password')
        self.authenticated_user = user
        return self.cleaned_data
    def get_user(self):
        return self.authenticated_user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']


class PaymentIntentForm(forms.Form):
    amount = forms.DecimalField(label='Amount (USD)', max_digits=10, decimal_places=2) 

class PaymentMethodForm(forms.Form):
    payment_method_id = forms.CharField(widget=forms.HiddenInput())