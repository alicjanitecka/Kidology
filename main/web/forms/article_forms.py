from django import forms
from django.forms import ModelForm
from ...models import Article, Category, AgeGroup


class ArticleForm(ModelForm):

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    age_groups = forms.ModelMultipleChoiceField(
        queryset=AgeGroup.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'categories', 'age_groups']


class ArticleSearchForm(forms.Form):
    search_query = forms.CharField(required=False, label='Szukaj')
    search_in_title = forms.BooleanField(required=False, initial=True, label='Szukaj wg tytułu')
    search_in_content = forms.BooleanField(required=False, initial=False, label='Szukaj wg treści')
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Kategorie'
    )
    age_groups = forms.ModelMultipleChoiceField(
        queryset=AgeGroup.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Grupy wiekowe'
    )