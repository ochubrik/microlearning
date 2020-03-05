from django.urls import path
from django.contrib.auth import views as au_views
from . import views
from django.urls import reverse_lazy

app_name = 'mainpage'


class MyHackedView(au_views.PasswordResetView):
    success_url = reverse_lazy('registration:password_reset_done')


urlpatterns = [
    path('login/', au_views.LoginView.as_view(), name='login'),
    path('logout/', au_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', MyHackedView.as_view(), name='password_reset'),
    path('password_reset/done/', au_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', au_views.PasswordResetConfirmView.as_view(
         success_url=reverse_lazy('registration:password_reset_complete')),
         name='password_reset_confirm'
         ),
    path('reset/done/', au_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
