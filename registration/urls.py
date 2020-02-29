from django.urls import path
from . import views

app_name = 'mainpage'
urlpatterns = [
    path('accounts/', views.mainpage, name='mainpage'),
]