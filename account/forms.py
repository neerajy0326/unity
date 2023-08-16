from django import forms

from .models import CustomUser, GENDER_CHOICES, ACCOUNT_TYPE_CHOICES

class UserRegistrationForm(forms.ModelForm):


    full_name = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    contact_number = forms.CharField(widget=forms.TextInput)
    username = forms.CharField(widget=forms.TextInput)
    date_of_birth = forms.DateField() , 
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE_CHOICES, widget=forms.Select)
   
    class Meta:
        model = CustomUser
        fields = ['full_name', 'contact_number', 'email', 'username', 'date_of_birth', 'gender', 'account_type', 'password']

   
