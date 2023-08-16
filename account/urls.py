from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('open_account', views.open_account, name='open_account'),
    path('login_page', views.login_page, name='login_page'),
    path('profile' ,views.profile , name='profile'),
    path('logout', views.logout_view, name='logout'),
    path('profile/transfer_money', views.transfer_money, name='transfer_money'),
    path('profile/transfer_money/enter_pin', views.enter_pin, name='enter_pin'),

    
  

    
]