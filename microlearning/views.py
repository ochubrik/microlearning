from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models
from .models import Article


# articles_num = Article.objects.all().count()
@login_required
def article_index(request):
    return render(request, 'article/index.html')
    # context={'articles_num': articles_num},)


@login_required
def article_list(request):
    return render(request, 'article/list.html', {
        'articles': Article.objects.all()})


@login_required
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
