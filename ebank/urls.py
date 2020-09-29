from django.urls import path
from ebank import views

urlpatterns = [
    path('', views.index, name='home'),
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login_user, name='login'),
    path('api/init-transfer/', views.init_transfer, name='init-transfer'),
    path('api/transfer/', views.transfer, name='transfer'),
    path('api/buy-airtime/', views.buy_airtime, name='buy-airtime'),
]
