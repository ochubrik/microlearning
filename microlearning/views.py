from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from . import models, forms
from .models import Article
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView




@login_required
def article_index(request):
    available_article_list = request.user.profile.get_my_articles()

    return render(request, 'article/index.html',
                  {
                      'articles': available_article_list
                  })


@login_required
class ArticleListView(LoginRequiredMixin, ListView):
    queryset = models.Article.objects.all()
    context_object_name = 'articles'
    template_name = 'article/list.html'

@login_required
def article_list(request):
    context = {}

    article_list = Article.objects.all().order_by('-publish')
    paginator = Paginator(article_list, 15)

    page_number = request.GET.get('page', 1)
    articles = paginator.get_page(page_number)

    return render(request, 'article/list.html', {
        'articles': articles
    })


@login_required
def article_details(request, type: str, id_med: int, slug: str):
    article = get_object_or_404(models.Article,
                                status="new",
                                type=type,
                                id_med=id_med,
                                slug=slug)

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
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

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
        user_form.save()

        return redirect('microlearning:edit')
    else:
        user_form = forms.UserEditForm(instance=request.user)

    return render(request, 'edit.html', {
        'user_form': user_form,
    })


@login_required
def view_profile(request):
    return render(request, 'profile.html', {'user': request.user})
