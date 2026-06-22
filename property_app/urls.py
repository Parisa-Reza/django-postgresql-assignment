from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_listing, name='property_listing'),
    path('properties/<slug:slug>/', views.property_detail, name='property_detail')

]

