from django.shortcuts import render, get_object_or_404

from . import models


# Create your views here.

# def mainpage(request):
#     return render(request,
#                   'article/mainpage.html')


def all_articles(request):
    article_list = models.Article.objects.all()
    return render(request,
                  'article/list.html',
                  {"articles": article_list})


def article_details(request, year, month, day, slug):
    article = get_object_or_404(models.Article,
                                slug=slug,
                                status="new",
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    return render(request,
                  'article/detail.html',
                  {'article': article})
