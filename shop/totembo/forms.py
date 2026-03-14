from django import forms

from .models import Category, Order
from django_svg_image_form_field import SvgAndImageFormField
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        field_classes = {
            'icon': SvgAndImageFormField,
        }


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email:', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким email не найден.")
        return username


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email:', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    first_name = forms.CharField(label='Имя:', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Фамилия:', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password1 = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    password2 = forms.CharField(label='Подтверждение пароля:', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(username=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Use email as username
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'address',
            'city',
            'region',
            'phone',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия...'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш адрес...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш город...'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш регион...'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш телефон...'}),
        }


