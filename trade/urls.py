from django.urls import path
from . import views

urlpatterns = [
    path('add_trade/', views.add_trade, name='add_trade'),
    path('delete_trade/', views.delete_trade, name='delete_trade'),
    path('get_trades/', views.get_trades, name='get_trades'),
]
