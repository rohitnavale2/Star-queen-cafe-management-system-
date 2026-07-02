from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.events, name='events'),
    path('visit/', views.visit, name='visit'),
    path('reservation/', views.reservation, name='reservation'),

    # ── HOME DELIVERY ──
    path('order/', views.delivery_home, name='delivery_home'),
    path('order/place/', views.place_order, name='place_order'),
    path('order/confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    path('order/receipt/<str:order_number>/', views.receipt_download, name='receipt_download'),
    path('order/track/', views.track_order, name='track_order'),
    path('order/check-area/', views.check_delivery_area, name='check_delivery_area'),

    # ── RAZORPAY PAYMENT ──
    path('payment/verify/', views.payment_verify, name='payment_verify'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
]
