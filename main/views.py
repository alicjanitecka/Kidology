from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Article, Category, AgeGroup
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from .forms import ArticleSearchForm
from django.db.models import Q
from django import forms
from django.forms import ModelForm


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

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'kidology/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Rejestracja zakończona pomyślnie. Możesz się teraz zalogować.')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'kidology/login.html'
    # success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        messages.success(self.request, 'Zalogowano pomyślnie.')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Niepoprawny adres e-mail lub hasło.')
        return super().form_invalid(form)

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'kidology/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.all()
        form = ArticleSearchForm(self.request.GET)

        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            search_in_title = form.cleaned_data.get('search_in_title')
            search_in_content = form.cleaned_data.get('search_in_content')
            categories = form.cleaned_data.get('categories')
            age_groups = form.cleaned_data.get('age_groups')

            if search_query:
                query = Q()
                if search_in_title:
                    query |= Q(title__icontains=search_query)
                if search_in_content:
                    query |= Q(content__icontains=search_query)
                if query:
                    queryset = queryset.filter(query)

            if categories:
                queryset = queryset.filter(categories__in=categories).distinct()
            if age_groups:
                queryset = queryset.filter(age_groups__in=age_groups).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ArticleSearchForm(self.request.GET)
        return context

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'kidology/article_detail.html'

class ArticleCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Article
    template_name = 'kidology/article_form.html'
    form_class = ArticleForm
    success_url = reverse_lazy('article_list')

class ArticleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Article
    template_name = 'kidology/article_form.html'
    form_class = ArticleForm
    success_url = reverse_lazy('article_list')

class ArticleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Article
    template_name = 'kidology/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')

