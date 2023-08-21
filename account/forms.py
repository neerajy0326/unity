from django import forms

from .models import CustomUser, CardRequest , GENDER_CHOICES, ACCOUNT_TYPE_CHOICES , PROFESSION_CHOICES

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

class CardApprovalForm(forms.Form):
    approval_status = forms.ChoiceField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected')], widget=forms.RadioSelect)
    card_balance = forms.DecimalField(label='Card Balance', required=False) 


class CardRequestForm(forms.ModelForm):
    profession = forms.ChoiceField(choices=PROFESSION_CHOICES , widget=forms.Select)
    class Meta:
        model = CardRequest
        fields = ['salary' , 'profession'  , 'card_limit' ] 


         
