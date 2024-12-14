from .views import *
from django.urls import path


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shoe/<int:shoe_id>/', ShoeDetailView.as_view(), name='shoe_detail'),
    path('cart/add/<int:shoe_id>/', add_to_cart, name='add_to_cart'), 
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', ViewCart.as_view(), name='view_cart'),
    path('add-shoe/', add_shoe, name='add_shoe'),
]
