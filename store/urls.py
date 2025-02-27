from django.urls import path
from . import views
from .views import PaymentView, AddCouponView

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('product/<str:slug>/', views.detail_product, name='product'),
    path('order-summary/', views.order_summary, name='order-summary'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('add-to-cart/<str:slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<str:slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('add-single-item-to-cart/<str:slug>/', views.add_single_item_to_cart, name='add-single-item-to-cart'),
    path('remove-single-item-from-cart/<str:slug>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('delete-from-cart/<str:slug>/', views.delete_from_cart, name='delete-from-cart'),
]
