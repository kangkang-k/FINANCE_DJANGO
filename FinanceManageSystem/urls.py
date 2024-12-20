from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userpro/', include('userpro.urls')),
    path('account/', include('account.urls')),
    path('budget/', include('budget.urls')),
    path('trade/', include('trade.urls')),
]
