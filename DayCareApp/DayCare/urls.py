from django.urls import path, include

from DayCareApp.DayCare import views

urlpatterns = (
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('index/<int:profile_id>/', views.login_index, name='login_index'),
    path('', views.log_out, name='logout'),
)
