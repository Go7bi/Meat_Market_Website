from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import CardDetails
from django import forms
from django.core.validators import RegexValidator

class CustomUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']



class PaymentForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    payment_method = forms.ChoiceField(choices=[('cod', 'Cash on Delivery'), ('online', 'Online Payment')])

class CardForm(forms.ModelForm):
    
        model = CardDetails
        fields = ('card_number', 'expiration_date', 'cvv', 'cardholder_name')
        widgets = {
            'card_number': forms.TextInput(attrs={'placeholder': 'XXXX XXXX XXXX XXXX'}),
            'expiration_date': forms.DateInput(attrs={'type': 'month', 'placeholder': 'MM/YY'}),
            'cvv': forms.TextInput(attrs={'placeholder': 'XXX'}),
            'cardholder_name': forms.TextInput(attrs={'placeholder': 'Cardholder Name'})
        }
