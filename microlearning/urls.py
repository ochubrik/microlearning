from django.urls import path
from . import views

app_name = 'microlearning'
urlpatterns = [
    path('', views.article_index, name='article_index'),
    path('<str:type>/<int:id_med>-<slug:slug>',
         views.article_details,
         name='article_details'),
    path('list_articles/', views.article_list, name='article_list'),
    path('settings/', views.settings, name='settings'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]