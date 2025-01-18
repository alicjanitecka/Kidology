from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Article
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='Admin').exists()

class SignUpView(CreateView):
    form_class = UserCreationForm
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
    success_url = reverse_lazy('article_list')

    def form_invalid(self, form):
        messages.error(self.request, 'Niepoprawny adres e-mail lub hasło.')
        return super().form_invalid(form)

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'kidology/article_list.html'
    context_object_name = 'articles'

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'kidology/article_detail.html'

class ArticleCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Article
    template_name = 'kidology/article_form.html'
    fields = ['title', 'content', 'category', 'age_group']
    success_url = reverse_lazy('article_list')

class ArticleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Article
    template_name = 'kidology/article_form.html'
    fields = ['title', 'content', 'category', 'age_group']
    success_url = reverse_lazy('article_list')

class ArticleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('article_list')
