from django.urls import path
from . import views

app_name = 'microlearning'
urlpatterns = [
    path('', views.article_index, name='article_index'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.article_details,
         name='article_details'),
    path('list_articles/', views.article_list, name='article_list'),
]