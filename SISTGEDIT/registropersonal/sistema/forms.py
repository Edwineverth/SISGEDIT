from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cargo


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.') # noqa
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.') # noqa
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.') # noqa
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    bio = forms.CharField(max_length=200, required=False, help_text='Optional.', widget= forms.Textarea) # noqa
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all())

    numerotelefono = forms.CharField(max_length=10, required=False, help_text='Optional.') # noqa

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'bio', 'birth_date', 'cargo', 'numerotelefono', ) # noqa
