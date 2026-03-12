from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    college = forms.CharField(max_length=200, required=False)
    role = forms.ChoiceField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')])

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'college', 'role', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'college', 'bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
