from django.urls import path, include
from . import views as portfolio_view
from froala_editor import views

urlpatterns = [
    path('', portfolio_view.index, name='index'),
    path('user_signup/', portfolio_view.user_signup, name='user_signup'),
    path('user_login/', portfolio_view.user_login, name='user_login'),
    path('user_logout/', portfolio_view.user_logout, name='user_logout'),
    path('tech_details/<int:tech_id>', portfolio_view.tech_details, name='tech_details'),
    path('new_client_feed/', portfolio_view.new_client_feed, name='new_client_feed'),
    path('contact_us/', portfolio_view.contact_us, name='contact_us'),
    path('about_me/', portfolio_view.about_me, name='about_me'),
    path('user_portfolio/', portfolio_view.user_portfolio, name='user_portfolio'),
    path('user_profile_details/<int:user_id>', portfolio_view.user_profile_details, name='user_profile_details'),
    path('froala_editor/',include('froala_editor.urls'))
]
