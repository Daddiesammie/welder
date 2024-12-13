from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about, name='about'),
    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    path('quote-request/', views.quote_request, name='quote_request'),
    path('quote-success/', views.quote_success, name='quote_success'),
    path('contact/', views.contact, name='contact'),
    path('contact-success/', views.contact_success, name='contact_success'),
    path('track/', views.track_quote, name='track_quote'),

]
