from django.urls import path, include

from DayCareApp.DayCare import views

urlpatterns = (
    path('', views.index, name='index'),
)