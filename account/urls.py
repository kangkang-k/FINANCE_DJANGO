from django.urls import path
from . import views

urlpatterns = [
    path('add_account/', views.add_account, name='add_account'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('get_user_accounts/', views.get_user_accounts, name='get_user_accounts'),
    path('update_account/', views.update_account, name='update_account'),
    path('get_account_details/', views.get_account_details, name='get_account_details'),
]
