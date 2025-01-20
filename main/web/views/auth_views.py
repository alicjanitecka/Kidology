from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from ..forms.auth_forms import CustomUserCreationForm, CustomAuthenticationForm


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
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        messages.success(self.request, 'Zalogowano pomyślnie.')
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form data:", form.cleaned_data)
        print("Form errors:", form.errors)
        print("User cache:", getattr(form, 'user_cache', None))
        messages.error(self.request, 'Niepoprawny adres e-mail lub hasło.')
        return super().form_invalid(form)

    def get_success_url(self):
        return self.success_url
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Wylogowano pomyślnie.')
        messages.get_messages(request).used = True
        return super().dispatch(request, *args, **kwargs)