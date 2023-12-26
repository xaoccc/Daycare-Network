from django.urls import path, include

from DayCareApp.DayCare import views

urlpatterns = (
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('index/', views.login_index, name='login_index'),
    path('', views.log_out, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('settings/username_edit/', views.username_edit, name='username_edit'),
    path('settings/password_edit/', views.password_edit, name='password_edit'),
    path('users/', views.user_data, name='user_data'),
    path('services/', views.services, name='services'),
    path('offers/', views.offers, name='offers'),
    path('register-offer/', views.register_offer, name='register_offer'),
    path('deleted/', views.delete_user, name='delete_user'),
    path('job_offers/', views.find_offers, name='find_offers'),
)
