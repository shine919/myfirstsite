from django import forms
from .models import *
from django.contrib.auth.models import User

Payment_Choices =(
    ("1","Наличными"),
    ("2","Картой"),
)
class CheckoutContactForm(forms.Form):
    name = forms.CharField(required=True)
    payment = forms.ChoiceField(choices = Payment_Choices,required=True)
    address = forms.CharField(required=True)
    phone = forms.CharField(required=True)
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            self.user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(f'Пользватель с таким именем {username} не существует')
        if not self.user.check_password(password):
            raise forms.ValidationError(f'Пароль неверен для пользователя {username}')
        return cleaned_data
class RegisterForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].required= True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class']= 'form-input'
    class Meta:
        model = User
        fields = ('username','email','password')
        widgets = {
            'username':forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
            'email': forms.TextInput(attrs={'placeholder': 'Адрес электронной почты'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        }