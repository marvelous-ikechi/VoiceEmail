from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.home_page, name='home'),
    path('compose/', views.send_mail, name='compose'),
    path('inbox/', views.view_mail, name='inbox'),
    path('trash/', views.delete_mail, name='trash'),
    path('logout/', views.log_out, name='logout'),
]