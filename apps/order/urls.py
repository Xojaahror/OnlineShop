from django.urls import path
from .views import (OpenCartView, 
                    OpenWishlistView, 
                    CreateWishlistView, 
                    CreateCartView, 
                    DeleteCartItemView, 
                    DeleteWishlistItemView, 
                    DeleteWishlistView)

app_name = 'order'

urlpatterns = [
    path('create-wishlist/<uuid:uuid>', CreateWishlistView.as_view(), name="create_wishlist"),
    path('create-cart/<uuid:uuid>', CreateCartView.as_view(), name="create_cart"),
    path('delete-cart-item/<uuid:uuid>', DeleteCartItemView.as_view(), name='delete_cart_item'),
    path('delete-wishlist-item/<uuid:uuid>', DeleteWishlistItemView.as_view(), name='delete_wishlist_item'),
    path('delete-wishlist/', DeleteWishlistView.as_view(), name="delete_wishlist"),
    path('view-wishlist/', OpenWishlistView.as_view(), name="open_wishlist"),
    path('view-cart/', OpenCartView.as_view(), name="open_cart"),

]
