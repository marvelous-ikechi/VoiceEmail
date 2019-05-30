from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='home'),
    path('mails/', views.view_mail, name='mails'),
    path('home/', views.home_page, name='home'),
]