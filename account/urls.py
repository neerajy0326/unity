from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('open_account', views.open_account, name='open_account'),
    path('login', views.login, name='login'),

    
]