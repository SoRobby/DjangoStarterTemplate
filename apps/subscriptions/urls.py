from django.urls import path

from . import views

app_name = 'subscriptions'

# Root url of "roadmap" is 'roadmap/', defined in config.urls.py
urlpatterns = [
    path('', views.subscription_plans, name='subscription-plans'),

    path('purchase/checkout/<str:term_uuid>/', views.CheckoutSessionCreateView.as_view(), name='subscription-checkout'),

    path('purchase/checkout/<str:term_uuid>/orders/<str:order_uuid>/cancel/', views.CheckoutSessionCancelView.as_view(),
         name='subscription-checkout-cancel')

]
