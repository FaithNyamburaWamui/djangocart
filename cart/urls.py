# cart/urls.py
from django.urls import path
from .views import complete_purchase  # Import the view functions

urlpatterns = [
    path('complete_purchase/', complete_purchase, name='complete_purchase'),
]
