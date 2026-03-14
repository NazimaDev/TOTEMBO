from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('category/<slug:slug>/', CategoryDetail.as_view(), name='category_detail'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product'),
    path('authentication/', login_register_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('cart/', cart_view, name='cart'),
    path('to_cart/<int:pk>/add/', add_to_cart, name='cart_add'),
    path('to_cart/<int:pk>/remove/', remove_from_cart, name='cart_remove'),
    path('to_cart/<int:pk>/delete/', delete_from_cart, name='cart_delete'),
    path('clear_cart/', clear_cart, name='cart_clear'),
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/success/', checkout_success_view, name='checkout_success'),
    path('favorites/', favorites_view, name='favorites'),
    path('favorites/add/<int:pk>/', add_to_favorites, name='favorite_add'),
    path('favorites/remove/<int:pk>/', remove_from_favorites, name='favorite_remove'),
    path('search/', search_view, name='search'),
    path('subscribe/', subscribe_email, name='subscribe_email'),
    path('contact/', contact_view, name='contact'),
    path('privacy/', privacy_view, name='privacy'),
    path('faq/', faq_view, name='faq'),
]
