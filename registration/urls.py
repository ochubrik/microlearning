from django.contrib.auth import views as au_views
from django.urls import reverse_lazy

app_name = 'mainpage'


class MyHackedView(au_views.PasswordResetView):
    success_url = reverse_lazy('registration:password_reset_done')


urlpatterns = [

]
