from django.shortcuts import render , redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import get_user_model ,authenticate
import random
from .models import CustomUser
from django.contrib.auth import authenticate, login ,logout 
from decimal import Decimal

def home_page(request):
    return render(request, 'index.html')

def generate_unique_account_number():
    while True:
        account_number = str(random.randint(1000, 9999))
        if not CustomUser.objects.filter(account_number=account_number).exists():
            return account_number

def open_account(request):   
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print(form.errors)
            email = form.cleaned_data['email']
            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, 'User with this email address already exists.')
                return redirect('register')

            full_name = form.cleaned_data['full_name']
            contact_number = form.cleaned_data['contact_number']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            date_of_birth = form.cleaned_data['date_of_birth']
            gender = form.cleaned_data['gender']
            account_type = form.cleaned_data['account_type']
            ifsc = random.choice(['UFB01', 'UFB02', 'UFB03'])


            user = get_user_model().objects.create_user(
                email=email, contact_number=contact_number, full_name=full_name, username=username, 
                date_of_birth=date_of_birth, gender=gender, account_type=account_type , ifsc=ifsc
            )
            user.set_password(password)
            account_number = generate_unique_account_number()
            user.account_number = account_number
            user.save()
            
            messages.success(request, 'Account has been successfully created for user ' + full_name)
            return redirect('login_page')
        else:
            

            messages.error(request, 'Username not available. Choose different one!')
    else:
        form = UserRegistrationForm()

    return render(request, 'open_account.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login_page.html')

def profile(request):
   
    return render(request,'profile.html')

def logout_view(request):
    logout(request) 
    return redirect('home_page')


def transfer_money(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        ifsc = request.POST.get('ifsc')
        
        amount = Decimal(request.POST.get('amount'))
        
       
        recipient = CustomUser.objects.filter(account_number=account_number, ifsc=ifsc).first()
        sender = request.user
        print(sender)
        print(recipient)

        if sender.balance is None:
            print("Sender balance is None")
        if recipient and sender.balance >= amount:

            amount_float = float(amount)
            
            request.session['transfer_details'] = {
                'user_id': recipient.id,  
                'amount': amount_float
            }
            print(recipient.id)
            return redirect('enter_pin') 
    
    return render(request, 'transfer_money.html')

def enter_pin(request):
    if request.method == 'POST':
        pin = request.POST.get('pin')
        transfer_details = request.session.get('transfer_details')
        if transfer_details:


            user_id = transfer_details['user_id']
            print(user_id)
            amount_float = transfer_details['amount']
            amount = Decimal(str(amount_float))
            sender = request.user
            print(sender)
            
            
            
            
            if pin == sender.pin: 
           
                recipient = CustomUser.objects.get(id=user_id)
                print(recipient)
                sender.balance -= amount
                recipient.balance += amount
                sender.save()
                recipient.save()
               
                
              
                del request.session['transfer_details']
                
               
                messages.success(request, 'Money transferred successfully!')
                return redirect('profile')  
            
            else:
                messages.error(request, 'Invalid PIN. Please try again.')
    
    return render(request, 'enter_pin.html')
    