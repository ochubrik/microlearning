from django import forms

from microlearning import models
from microlearning.models import Article
from django.contrib.auth.models import User


class UserSettingsForm(forms.Form):
    category = forms.ChoiceField(
        required=False,
        widget=forms.Select,  # CheckboxSelectMultiple,
        choices=Article.ARTICLE_TYPES,
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Pass',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('bad pass')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('subscribed_category',)

