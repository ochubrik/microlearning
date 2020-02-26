from django.urls import path
from . import views

app_name = 'microlearning'
urlpatterns = [
    # path('', views.mainpage, name='mainpage'),
    path('', views.all_articles, name='all_articles'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.article_details,
         name='article_details'),
]