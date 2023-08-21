from django.shortcuts import render , redirect
from .forms import UserRegistrationForm ,  CardRequestForm , CardApprovalForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model ,authenticate
import random
from .models import CustomUser , AccountTransaction , CardRequest, CardDetails
from django.contrib.auth import authenticate, login ,logout 
from decimal import Decimal
from django.db.models import Q
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string


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
    user = request.user
    transactions = AccountTransaction.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('-timestamp')[:10]
    try:
        card_details = CardDetails.objects.get(user=user)
    except CardDetails.DoesNotExist:
        card_details = None

    context = {
        'user': user,
        'transactions': transactions,
        'card_details': card_details
    }
    return render(request,'profile.html' , context)

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
                if sender == recipient:
                   return render(request, 'enter_pin.html', {'error_message': 'You cannot send money to yourself.'})
                sender.balance -= amount
                recipient.balance += amount
                sender.save()
                recipient.save()
                AccountTransaction.objects.create(sender=sender, recipient=recipient, amount=amount,timestamp=timezone.now())
                
              
                del request.session['transfer_details']
                
               
                messages.success(request, 'Money transferred successfully!')
                return redirect('profile')  
            
            else:
                messages.error(request, 'Invalid PIN. Please try again.')
    
    return render(request, 'enter_pin.html')

def edit_profile(request):
    return render(request, 'edit_profile.html')

def tandc(request):
    return render(request, 'tandc.html')

def generate_random_cvv():
    return get_random_string(length=3, allowed_chars='0123456789')

def admin_card_approval(request):
    if request.user.is_superuser:
        pending_card_requests = CardRequest.objects.filter(status="Pending")
        if request.method == 'POST':
            form = CardApprovalForm(request.POST)
            if form.is_valid():
                approval_status = form.cleaned_data['approval_status']
                card_request_id = request.POST.get('card_request_id')
                
                
                try:
                    card_request = CardRequest.objects.get(pk=card_request_id)
                except CardRequest.DoesNotExist:
                    messages.error(request, 'Card request not found.')
                else:    
                   card_request.status = approval_status
                   card_request.save()
                  

                   if approval_status == 'Approved':
                       card_balance = form.cleaned_data['card_balance']
                       
                       if card_balance is None:
                          messages.error(request, 'Please provide the card balance.')
                       else:
                        
                        card_number = get_random_string(length=16, allowed_chars='0123456789')
                        expiry_date = date.today().replace(year=date.today().year + 3) 
                        cvv = generate_random_cvv()
                        fee = Decimal('500.00')
                        card_request.user.balance -= fee
                        card_request.user.save()
                   
                        CardDetails.objects.create(user=card_request.user, card_number=card_number, expiry_date=expiry_date,cvv=cvv, card_balance=card_balance)

                        messages.success(request, 'Card request approved/rejected.')
        else:
            form = CardApprovalForm()
        return render(request, 'admin_approval.html', {'pending_card_requests': pending_card_requests, 'form': form})
    else:
        return redirect('profile')
    

def apply_page(request):
    user = request.user
    try:
        latest_card_request = CardRequest.objects.filter(user=user).latest('date_requested')
    except ObjectDoesNotExist:
        latest_card_request = None
    try:
        card_details = CardDetails.objects.get(user=user)
        
    except CardDetails.DoesNotExist:
        card_details = None
    print(card_details)    
    return render(request ,'apply_page.html' ,  {'card_request': latest_card_request , 'card_details': card_details})    


def user_request_card(request):
    
    if request.method == 'POST':
        form = CardRequestForm(request.POST)
        if form.is_valid():
            user_balance = request.user.balance
            if user_balance >= 500.00:
              card_request = form.save(commit=False)
              card_request.user = request.user
              card_request.save()
              return redirect('apply_page')
            else: 
                form.add_error(None , "You need a minimum balance of Rs. 500 to apply for a card.")
    else:
        form = CardRequestForm()
    
    return render(request, 'apply_card.html', {'form': form})



def card_details(request):
    user = request.user
    try:
        card_details = CardDetails.objects.get(user=user)
    except CardDetails.DoesNotExist:
        card_details = None

    context = {
        'card_details': card_details
    }
    return render(request, 'card_details.html' ,context)