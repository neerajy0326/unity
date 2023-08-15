from django.shortcuts import render


def home_page(request):
    return render(request, 'index.html')

def open_account(request):   
    return render(request, 'open_account.html')