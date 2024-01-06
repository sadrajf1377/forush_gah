from django.contrib.auth.models import AbstractUser
from django.urls import path

from user_Module import models
from .views import edit_user_info,ask_for_password_reset,change_password,user_messages,my_favourites,my_debts

urlpatterns=[path('edit_user_info/<pk>',edit_user_info.as_view(),name='edit_user_info')
             ,path('ask_for_password_reset',ask_for_password_reset.as_view(),name='ask_for_password_reset')
             ,path('reset_password/<reset_code>',change_password,name='reset_password')
             ,path('user_message/<pk>',user_messages.as_view(),name='load_user_messages')
             ,path('user_favourite_products/<pk>',my_favourites.as_view(),name='my_favourite_products')
            ,path('user_debts/<id>',my_debts.as_view(),name='my_debts')

             ]