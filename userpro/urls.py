from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='user_profile'),
    path('login/', views.login, name='login'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('get_user_info/', views.get_user_info, name='get_user_info'),
    path('logout/', views.logout_user, name='logout'),
]
