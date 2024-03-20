
from django.urls import path
from .views import custom_login, webhook, home, claim_points

urlpatterns = [
    path('login/', custom_login, name='login'),
    path('webhook/', webhook, name='webhook'),
    path('', home, name='home'),
    path('claim/', claim_points, name='claim_points'),
 
]
