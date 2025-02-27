from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        # Set placeholders for each field
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

        # Hide labels
        for field in self.fields.values():
            field.label = ''

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Email already exists!')
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
        }

class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username or Email'}),
        label='',
    )

    password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': 'Password'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if username_or_email and password:
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(username=username_or_email)
            except UserModel.DoesNotExist:
                try:
                    user = UserModel.objects.get(email=username_or_email)
                except UserModel.DoesNotExist:
                    raise forms.ValidationError('Invalid username or email')

            if not user.check_password(password):
                raise forms.ValidationError('Invalid password')

            cleaned_data['user'] = user

        return cleaned_data

