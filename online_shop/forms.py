from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import validate_email

from .models import Order, Mailing

User = get_user_model()


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе.')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Неверный пароль")
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username', 'password'
        ]


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['first_name'].label = 'Ваше имя'
        self.fields['last_name'].label = 'Ваша фамилия'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['email'].label = 'Электронная почта'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Данный почтовый адрес уже зарегестрирован в системе')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Логин {username} занято')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username', 'password', 'confirm_password', 'first_name', 'last_name', 'email', 'phone'
        ]


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = [
            'comment'
        ]


class PasswordCustomChangeForm(forms.ModelForm):

    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Старый пароль'
        self.fields['new_password'].label = 'Новый пароль'
        self.fields['confirm_password'].label = 'Подтвердите новый пароль'

    def clean(self):
        old_password = self.cleaned_data["old_password"]
        new_password = self.cleaned_data["new_password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if old_password == new_password:
            raise forms.ValidationError("Старый и новый пароли совпадают")

        if new_password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

        if not self.user.check_password(old_password):
            raise forms.ValidationError("Старый пароль введен неверно")

        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            "old_password", "new_password", "confirm_password"
        ]


class MailingForm(forms.ModelForm):

    email = forms.CharField(required=True)

    def clean(self):
        email = self.cleaned_data["email"]

        if validate_email(email):
            raise forms.ValidationError(f'Email введен неправильно')

        if Mailing.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Данный почтовый адрес уже зарегестрирован в рассылке')

        return self.cleaned_data

    class Meta:
        model = Mailing
        fields = [
            "email"
        ]
