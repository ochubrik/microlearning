from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models, forms
from .models import Article
from django.contrib.auth.models import User
from django.views.generic import ListView

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# from . import forms

# articles_num = Article.objects.all().count()
@login_required
def article_index(request):
    available_article_list = models.Article.published.all()
    return render(request, 'article/index.html',
                  {'articles': available_article_list})
    # context={'articles_num': articles_num},)


class ArticleListView(LoginRequiredMixin, ListView):
    queryset = models.Article.objects.all()
    context_object_name = 'articles'
    template_name = 'article/list.html'


def article_list(request):
    return render(request, 'article/list.html', {
        'articles': Article.objects.all()})


# @login_required
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


def settings(request):
    if request.method == 'POST':
        user_setting_form = forms.UserSettingsForm(request.POST)
    else:
        user_setting_form = forms.UserSettingsForm

    return render(request, 'article/settings.html', {'form': user_setting_form})
