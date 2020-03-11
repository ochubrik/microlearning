from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from . import models, forms
from .models import Article
from django.contrib.auth.models import User
from django.views.generic import ListView

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from registration import forms


# from . import forms

# articles_num = Article.objects.all().count()
@login_required
def article_index(request):
    available_article_list = request.user.profile.get_my_articles()

    return render(request, 'article/index.html',
                  {'articles': available_article_list})


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


@login_required
def settings(request):
    if request.method == 'POST':
        user_setting_form = forms.UserSettingsForm(request.POST)
        if user_setting_form.is_valid():
            form_data = user_setting_form.cleaned_data

            request.user.profile.subscribed_category = form_data['category']
            request.user.save()

            return redirect('microlearning:settings')
    else:
        user_setting_form = forms.UserSettingsForm({
            'category': request.user.profile.subscribed_category,
        })

    return render(request, 'article/settings.html', {'form': user_setting_form})


def register(request):
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'],
            )
            new_user.save()
            # models.Profile.objects.create(user=new_user,
            #                               photo='unknown.jpeg')
            return render(request, 'registration_done.html', {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request,
                  'register.html',
                  {'form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = forms.UserEditForm(instance=request.user,
                                       data=request.POST)
        # profile_form = forms.ProfileEditForm(instance=request.user.profile,
        #                                      data=request.POST,
        #                                      files=request.FILES)
        user_form.save()
        # profile_form.save()
    else:
        user_form = forms.UserEditForm(instance=request.user)
        # profile_form = forms.ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'edit.html',
                  {'user_form': user_form,})
                   # 'profile_form': profile_form})