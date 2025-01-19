from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Category, AgeGroup

class CustomUserCreationForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=True)
    # last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Hasło musi mieć co najmniej 15 znaków.")
        return password1

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

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