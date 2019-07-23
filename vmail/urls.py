from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home_page, name='home'),
    path('compose/', views.compose_view, name='compose'),
    path('inbox/', views.view_mail, name='inbox'),
    path('trash/<int:mid>/', views.delete_mail, name='trash'),
    path('logout/', views.log_out, name='logout'),
    path('send_mail/', views.send_mail, name='send_mail'),
    path('details/<str:mid>/', views.details, name='details'),
]