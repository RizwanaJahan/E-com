from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('base/', views.HomePage, name='base'),
    path('login/', views.LOGIN, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registration/', views.REGISTRATION, name='registration'),
    path('success/', views.success, name='success'),
    path('token/', views.token_send, name='token_send'),
    path('error/', views.error, name='error'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('', views.MAIN, name='main'),
    path('product/<pk>', views.PRODUCT, name='product'),
    path('checkout/', views.checkout, name='checkout'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
