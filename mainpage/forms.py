from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField

from .models import *


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class RegForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}), max_length=200,
        label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                                max_length=300,
                                label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}), max_length=300,
        label='')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Эл. адрес'}),
                            required=False, label='')
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='', max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                               max_length=300, label='')
    captcha = CaptchaField(label='')


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(label='', max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='', max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Эл. адрес'}),
                            required=False, label='')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'avatar')
