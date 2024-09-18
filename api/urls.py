from django.urls import path
from .views import MaterialListView
from .views import CartListView
from .views import OrderDetailView
from .views import OrderListView



urlpatterns=[
    path("materials/", MaterialListView.as_view(), name="material_list_view"),
    path('cart/', CartListView.as_view(), name='cart'),
    path("orders/", OrderListView.as_view(), name = "order_list_view"),
    path("order/<int:id>/", OrderDetailView.as_view(), name = "order_detail_view"),  
]