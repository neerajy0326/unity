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
    path('profile/transfer_money/edit_profile', views.edit_profile, name='edit_profile'),
    path('profile/admin_card_approval', views.admin_card_approval, name='admin_card_approval'),
    path('profile/apply_page', views.apply_page, name='apply_page'),
    path('profile/user_request_card', views.user_request_card, name='user_request_card'),
    path('profile/card_details', views.card_details, name='card_details'),


    


    
  

    
]