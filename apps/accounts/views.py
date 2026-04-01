from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.views.generic import CreateView, View
from django.urls import reverse_lazy


class RegisterView(CreateView):
    """Регистрация пользователя"""
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Аккаунт успешно создан! Теперь вы можете войти.')
        return super().form_valid(form)


class CustomLoginView(LoginView):
    """Вход пользователя"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f'С возвращением, {form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Выход пользователя"""
    next_page = 'core:home'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы вышли из аккаунта')
        return super().dispatch(request, *args, **kwargs)


register_view = RegisterView.as_view()
login_view = CustomLoginView.as_view()
logout_view = CustomLogoutView.as_view()
