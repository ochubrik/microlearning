from django import forms

from microlearning.models import Article


class UserSettingsForm(forms.Form):
    category = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Article.ARTICLE_TYPES,
    )

