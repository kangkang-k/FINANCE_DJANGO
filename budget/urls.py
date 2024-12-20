from django.urls import path
from . import views

urlpatterns = [
    path('add_budget/', views.add_budget, name='add_budget'),
    path('delete_budget/', views.delete_budget, name='delete_budget'),
    path('update_budget/', views.update_budget, name='update_budget'),
    path('get_user_budgets/', views.get_user_budgets, name='get_user_budgets'),
    path('get_budget_detail/', views.get_budget_detail, name='get_budget_detail'),
]
