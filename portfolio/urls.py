from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('tech_details/<int:tech_id>', views.tech_details, name='tech_details'),
    path('new_client_feed/', views.new_client_feed, name='new_client_feed')
]
